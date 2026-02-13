"""
Fetch real salary data from BLS OES API v2.

Pulls data for all 313 occupations across 50 US metros. With a registered API key:
  - 500 requests/day, 50 series/request = 25,000 data points/day
  - Full pull needs ~2,200 requests = ~5 daily runs

Progress is saved between runs. Just re-run each day until complete.
Real BLS data replaces generated estimates in salary_data.json.
"""

import json
import os
import sys
import time
import urllib.request
import ssl

# Add this directory to path so we can import occupation/metro lists
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_full_data import OCCUPATIONS, US_METROS

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(DATA_DIR, "..", "next-app", "src", "lib")
PROGRESS_FILE = os.path.join(DATA_DIR, "api_progress.json")
SALARY_DATA_FILE = os.path.join(OUTPUT_DIR, "salary_data.json")

BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
API_KEY = os.environ.get("BLS_API_KEY", "")  # Get free key at https://data.bls.gov/registrationEngine/
BATCH_SIZE = 50        # max series per request with key
DAILY_LIMIT = 99999    # let the API enforce its own limits
DATA_YEAR = "2024"     # latest available OES data

# BLS OES data type codes
DATA_TYPES = {
    "01": "employment",
    "04": "mean_annual",
    "13": "median_annual",
    "11": "pct10_annual",
    "12": "pct25_annual",
    "14": "pct75_annual",
    "15": "pct90_annual",
}


def build_series_id(area_code, occ_code, dtype_code):
    """Build a BLS OES series ID.

    Format: OEUM + area(7) + industry(6) + occupation(6) + datatype(2) = 25 chars
    """
    area_padded = str(area_code).zfill(7)
    occ_clean = occ_code.replace("-", "")
    return f"OEUM{area_padded}000000{occ_clean}{dtype_code}"


def fetch_batch(series_ids):
    """Send one API request for a batch of series IDs."""
    payload = json.dumps({
        "seriesid": series_ids,
        "startyear": DATA_YEAR,
        "endyear": DATA_YEAR,
        "registrationkey": API_KEY,
    }).encode("utf-8")

    req = urllib.request.Request(BLS_API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "User-Agent": "SalaryLens/1.0",
    })

    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_progress():
    """Load saved progress from previous runs."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"fetched_keys": {}, "requests_today": 0, "last_run_date": ""}


def save_progress(progress):
    """Save progress to disk."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def main():
    print("=" * 60)
    print("  SalaryLens — BLS Real Data Fetcher")
    print("=" * 60)

    # Build mapping: combo_key -> (occ_slug, occ_code, area_code, city_short, state, area_name)
    combos = {}
    for occ_tuple in OCCUPATIONS:
        slug, soc_code, name, _ = occ_tuple
        for metro_tuple in US_METROS:
            m_slug, m_code, m_full, m_short, m_state, _, _ = metro_tuple
            combo_key = f"{m_code}_{soc_code}"
            combos[combo_key] = {
                "occ_slug": slug,
                "occ_code": soc_code,
                "occ_name": name,
                "area_code": m_code,
                "area_name": m_full,
                "city_short": m_short,
                "state": m_state,
            }

    total_combos = len(combos)
    total_series = total_combos * len(DATA_TYPES)
    total_batches = (total_series + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"\n  Occupations:      {len(OCCUPATIONS)}")
    print(f"  US Metros:        {len(US_METROS)}")
    print(f"  Total combos:     {total_combos:,}")
    print(f"  Series to fetch:  {total_series:,}")
    print(f"  Batches needed:   {total_batches:,}")
    print(f"  Daily limit:      {DAILY_LIMIT} requests")
    days = (total_batches + DAILY_LIMIT - 1) // DAILY_LIMIT
    print(f"  Estimated days:   ~{days}")

    # Load progress
    progress = load_progress()
    fetched = progress["fetched_keys"]  # key -> {dtype: value, ...}

    # Reset daily counter if it's a new day
    today = time.strftime("%Y-%m-%d")
    if progress.get("last_run_date") != today:
        progress["requests_today"] = 0
        progress["last_run_date"] = today

    requests_today = progress["requests_today"]

    # Figure out what we still need
    all_series = []  # list of (series_id, combo_key, dtype_code)
    for combo_key, info in combos.items():
        existing = fetched.get(combo_key, {})
        for dtype_code, dtype_name in DATA_TYPES.items():
            if dtype_name not in existing:
                sid = build_series_id(info["area_code"], info["occ_code"], dtype_code)
                all_series.append((sid, combo_key, dtype_code))

    fetched_count = sum(len(v) for v in fetched.values())
    print(f"\n  Already fetched:  {fetched_count:,} data points ({len(fetched):,} combos started)")
    print(f"  Remaining:        {len(all_series):,} series")
    print(f"  Requests used today: {requests_today}")

    if not all_series:
        print("\n  All data fetched! Building output...")
    else:
        remaining_requests = DAILY_LIMIT - requests_today
        if remaining_requests <= 0:
            print(f"\n  Daily limit already reached. Run again tomorrow!")
            _build_output(fetched, combos)
            return

        # Batch the remaining series
        batches = []
        for i in range(0, len(all_series), BATCH_SIZE):
            batches.append(all_series[i:i + BATCH_SIZE])

        batches_to_run = min(len(batches), remaining_requests)
        print(f"  Will fetch {batches_to_run} batches this run\n")

        successful = 0
        errors = 0

        for batch_idx in range(batches_to_run):
            batch = batches[batch_idx]
            sids = [item[0] for item in batch]

            # Build lookup
            sid_map = {}
            for sid, combo_key, dtype_code in batch:
                sid_map[sid] = (combo_key, dtype_code)

            pct = (batch_idx + 1) / batches_to_run * 100
            print(f"  [{batch_idx + 1}/{batches_to_run}] {pct:.0f}%  Fetching {len(sids)} series...", end=" ", flush=True)

            try:
                response = fetch_batch(sids)
                requests_today += 1

                if response.get("status") == "REQUEST_SUCCEEDED":
                    hits = 0
                    for series in response["Results"]["series"]:
                        sid = series["seriesID"]
                        if sid not in sid_map:
                            continue
                        combo_key, dtype_code = sid_map[sid]
                        dtype_name = DATA_TYPES[dtype_code]

                        if series["data"]:
                            val = series["data"][0]["value"]
                            # Skip special values
                            if val not in ("-", "*", "#", "**", "N", ""):
                                try:
                                    numeric = float(val.replace(",", ""))
                                    if combo_key not in fetched:
                                        fetched[combo_key] = {}
                                    fetched[combo_key][dtype_name] = int(numeric)
                                    hits += 1
                                except ValueError:
                                    pass
                        else:
                            # No data for this series — mark as checked so we don't retry
                            if combo_key not in fetched:
                                fetched[combo_key] = {}
                            fetched[combo_key][dtype_name] = None

                    successful += 1
                    print(f"+{hits} hits")
                else:
                    msgs = response.get("message", [])
                    # Check for rate limit
                    for msg in msgs:
                        if "threshold" in str(msg).lower() or "limit" in str(msg).lower():
                            print(f"RATE LIMITED")
                            print(f"\n  Daily limit reached. Progress saved.")
                            progress["fetched_keys"] = fetched
                            progress["requests_today"] = requests_today
                            save_progress(progress)
                            _build_output(fetched, combos)
                            return
                    errors += 1
                    print(f"FAILED: {msgs[0] if msgs else 'unknown'}")

                # Save progress every 10 batches
                if (batch_idx + 1) % 10 == 0:
                    progress["fetched_keys"] = fetched
                    progress["requests_today"] = requests_today
                    save_progress(progress)

                # Rate limit: ~2 requests/sec to be safe
                time.sleep(0.5)

            except Exception as e:
                errors += 1
                print(f"ERROR: {e}")
                if "429" in str(e) or "throttl" in str(e).lower():
                    print("  Rate limited! Saving progress...")
                    break
                time.sleep(2)

        # Save final progress
        progress["fetched_keys"] = fetched
        progress["requests_today"] = requests_today
        save_progress(progress)

        fetched_count = sum(1 for v in fetched.values() for val in v.values() if val is not None)
        combos_with_data = sum(1 for v in fetched.values() if any(val is not None for val in v.values()))
        print(f"\n  Batches: {successful} OK, {errors} errors")
        print(f"  Total data points: {fetched_count:,} across {combos_with_data:,} combos")

        remaining = len(all_series) - (batches_to_run * BATCH_SIZE)
        if remaining > 0:
            remaining_batches = (remaining + BATCH_SIZE - 1) // BATCH_SIZE
            remaining_days = (remaining_batches + DAILY_LIMIT - 1) // DAILY_LIMIT
            print(f"\n  ~{remaining_batches:,} batches remaining (~{remaining_days} more days)")
            print(f"  Run this script again tomorrow to continue!")

    _build_output(fetched, combos)


def _build_output(fetched, combos):
    """Merge real BLS data into salary_data.json, keeping generated data as fallback."""
    print(f"\n{'=' * 60}")
    print("  Merging real data into salary_data.json...")

    # Load existing data
    if not os.path.exists(SALARY_DATA_FILE):
        print("  ERROR: salary_data.json not found. Run generate_full_data.py first!")
        return

    with open(SALARY_DATA_FILE) as f:
        records = json.load(f)

    # Build lookup for existing records: (area_code, occ_slug) -> index
    record_index = {}
    for i, r in enumerate(records):
        key = f"{r['area_code']}_{r['occ_slug']}"
        record_index[key] = i

    # Map combo_key (area_code_occ_code) -> occ_slug for cross-referencing
    combo_to_slug = {}
    for combo_key, info in combos.items():
        combo_to_slug[combo_key] = info["occ_slug"]
        combo_to_slug[f"{info['area_code']}_{info['occ_slug']}"] = info["occ_slug"]

    updated = 0
    required = ["employment", "mean_annual", "median_annual",
                 "pct10_annual", "pct25_annual", "pct75_annual", "pct90_annual"]

    for combo_key, values in fetched.items():
        # Check if we have all required fields with real data
        real_vals = {k: v for k, v in values.items() if v is not None}
        if not all(f in real_vals for f in required):
            continue

        # Validate percentiles are in order
        p10, p25, med, p75, p90 = (
            real_vals["pct10_annual"], real_vals["pct25_annual"],
            real_vals["median_annual"], real_vals["pct75_annual"],
            real_vals["pct90_annual"]
        )
        if not (p10 <= p25 <= med <= p75 <= p90):
            continue

        # Find matching record in salary_data.json
        info = combos.get(combo_key)
        if not info:
            continue

        record_key = f"{info['area_code']}_{info['occ_slug']}"
        idx = record_index.get(record_key)
        if idx is None:
            continue

        # Update with real data
        for field in required:
            records[idx][field] = real_vals[field]
        updated += 1

    # Re-sort by median
    records.sort(key=lambda r: r["median_annual"], reverse=True)

    # Write
    with open(SALARY_DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

    file_size = os.path.getsize(SALARY_DATA_FILE) / (1024 * 1024)

    print(f"  Updated {updated:,} records with real BLS data")
    print(f"  Total records: {len(records):,}")
    print(f"  File size: {file_size:.1f} MB")

    if updated > 0:
        # Show some real data examples
        real_records = []
        for combo_key, values in fetched.items():
            real_vals = {k: v for k, v in values.items() if v is not None}
            if all(f in real_vals for f in required):
                info = combos.get(combo_key)
                if info:
                    real_records.append((info["occ_name"], info["city_short"], real_vals["median_annual"]))

        real_records.sort(key=lambda x: x[2], reverse=True)
        print(f"\n  Sample real BLS data:")
        for name, city, med in real_records[:10]:
            print(f"    ${med:>9,}  {name} — {city}")

    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
