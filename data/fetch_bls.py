"""
Fetch BLS OEWS salary data via the public API.
Builds series IDs for target metros x occupations, fetches in batches.
"""

import urllib.request
import json
import os
import ssl
import time

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Data type codes -> what they mean
# 01=employment, 03=mean_hourly, 04=mean_annual,
# 11=pct10_annual, 12=pct25_annual, 13=median_annual, 14=pct75_annual, 15=pct90_annual
WAGE_TYPES = {
    "01": "employment",
    "04": "mean_annual",
    "11": "pct10_annual",
    "12": "pct25_annual",
    "13": "median_annual",
    "14": "pct75_annual",
    "15": "pct90_annual",
}

# Top 50 US metro areas (MSA FIPS codes)
TOP_METROS = {
    "35620": "New York-Newark-Jersey City, NY-NJ-PA",
    "31080": "Los Angeles-Long Beach-Anaheim, CA",
    "16980": "Chicago-Naperville-Elgin, IL-IN-WI",
    "19100": "Dallas-Fort Worth-Arlington, TX",
    "26420": "Houston-The Woodlands-Sugar Land, TX",
    "47900": "Washington-Arlington-Alexandria, DC-VA-MD-WV",
    "33100": "Miami-Fort Lauderdale-Pompano Beach, FL",
    "37980": "Philadelphia-Camden-Wilmington, PA-NJ-DE-MD",
    "12060": "Atlanta-Sandy Springs-Alpharetta, GA",
    "14460": "Boston-Cambridge-Nashua, MA-NH",
    "38060": "Phoenix-Mesa-Chandler, AZ",
    "41860": "San Francisco-Oakland-Berkeley, CA",
    "40140": "Riverside-San Bernardino-Ontario, CA",
    "19820": "Detroit-Warren-Dearborn, MI",
    "42660": "Seattle-Tacoma-Bellevue, WA",
    "33460": "Minneapolis-St. Paul-Bloomington, MN-WI",
    "41740": "San Diego-Chula Vista-Carlsbad, CA",
    "45300": "Tampa-St. Petersburg-Clearwater, FL",
    "19740": "Denver-Aurora-Lakewood, CO",
    "41180": "St. Louis, MO-IL",
    "12580": "Baltimore-Columbia-Towson, MD",
    "34980": "Nashville-Davidson-Murfreesboro-Franklin, TN",
    "16740": "Charlotte-Concord-Gastonia, NC-SC",
    "36740": "Orlando-Kissimmee-Sanford, FL",
    "41700": "San Antonio-New Braunfels, TX",
    "38900": "Portland-Vancouver-Hillsboro, OR-WA",
    "40900": "Sacramento-Roseville-Folsom, CA",
    "38300": "Pittsburgh, PA",
    "17140": "Cincinnati, OH-KY-IN",
    "12420": "Austin-Round Rock-Georgetown, TX",
    "29820": "Las Vegas-Henderson-Paradise, NV",
    "26900": "Indianapolis-Carmel-Anderson, IN",
    "28140": "Kansas City, MO-KS",
    "18140": "Columbus, OH",
    "17460": "Cleveland-Elyria, OH",
    "41940": "San Jose-Sunnyvale-Santa Clara, CA",
    "27260": "Jacksonville, FL",
    "47260": "Virginia Beach-Norfolk-Newport News, VA-NC",
    "39300": "Providence-Warwick, RI-MA",
    "33340": "Milwaukee-Waukesha, WI",
    "36420": "Oklahoma City, OK",
    "39580": "Raleigh-Cary, NC",
    "32820": "Memphis, TN-MS-AR",
    "40060": "Richmond, VA",
    "31140": "Louisville/Jefferson County, KY-IN",
    "41620": "Salt Lake City, UT",
    "25540": "Hartford-East Hartford-Middletown, CT",
    "35380": "New Orleans-Metairie, LA",
    "13820": "Birmingham-Hoover, AL",
    "40380": "Rochester, NY",
}

# Top occupations (SOC codes) - high search volume jobs
TOP_OCCUPATIONS = {
    "11-1021": "General and Operations Managers",
    "11-2021": "Marketing Managers",
    "11-3021": "Computer and Information Systems Managers",
    "11-3031": "Financial Managers",
    "11-9111": "Medical and Health Services Managers",
    "13-1041": "Compliance Officers",
    "13-1071": "Human Resources Specialists",
    "13-1111": "Management Analysts",
    "13-1161": "Market Research Analysts and Marketing Specialists",
    "13-2011": "Accountants and Auditors",
    "13-2051": "Financial Analysts",
    "13-2072": "Loan Officers",
    "15-1211": "Computer Systems Analysts",
    "15-1212": "Information Security Analysts",
    "15-1232": "Computer User Support Specialists",
    "15-1241": "Computer Network Architects",
    "15-1244": "Network and Computer Systems Administrators",
    "15-1251": "Computer Programmers",
    "15-1252": "Software Developers",
    "15-1253": "Software Quality Assurance Analysts and Testers",
    "15-1254": "Web Developers",
    "15-1255": "Web and Digital Interface Designers",
    "15-1299": "Computer Occupations, All Other",
    "15-2031": "Operations Research Analysts",
    "15-2041": "Statisticians",
    "15-2051": "Data Scientists",
    "17-2051": "Civil Engineers",
    "17-2071": "Electrical Engineers",
    "17-2112": "Industrial Engineers",
    "17-2141": "Mechanical Engineers",
    "19-1042": "Medical Scientists, Except Epidemiologists",
    "21-1014": "Mental Health Counselors",
    "23-1011": "Lawyers",
    "23-2011": "Paralegals and Legal Assistants",
    "25-2021": "Elementary School Teachers, Except Special Education",
    "25-2031": "Secondary School Teachers",
    "27-1024": "Graphic Designers",
    "27-3031": "Public Relations Specialists",
    "29-1051": "Pharmacists",
    "29-1071": "Physician Assistants",
    "29-1122": "Occupational Therapists",
    "29-1123": "Physical Therapists",
    "29-1141": "Registered Nurses",
    "29-1171": "Nurse Practitioners",
    "29-1215": "Family Medicine Physicians",
    "29-2061": "Licensed Practical and Licensed Vocational Nurses",
    "31-1131": "Nursing Assistants",
    "31-9092": "Medical Assistants",
    "33-2011": "Firefighters",
    "33-3051": "Police and Sheriff's Patrol Officers",
    "35-2014": "Cooks, Restaurant",
    "35-3031": "Waiters and Waitresses",
    "37-2011": "Janitors and Cleaners",
    "41-2031": "Retail Salespersons",
    "41-3031": "Securities and Financial Services Sales Agents",
    "43-3031": "Bookkeeping, Accounting, and Auditing Clerks",
    "43-4051": "Customer Service Representatives",
    "43-6014": "Secretaries and Administrative Assistants",
    "47-2111": "Electricians",
    "47-2152": "Plumbers, Pipefitters, and Steamfitters",
    "49-3023": "Automotive Service Technicians and Mechanics",
    "49-9021": "HVAC Mechanics and Installers",
    "53-3032": "Heavy and Tractor-Trailer Truck Drivers",
}


def build_series_id(area_code, occ_code, datatype):
    """Build OEWS series ID: OE + U + M + area(7) + industry(6) + occ(6) + dtype(2) = 25 chars."""
    occ_clean = occ_code.replace("-", "")
    area_padded = area_code.ljust(7, "0")
    return f"OEUM{area_padded}000000{occ_clean}{datatype}"


def fetch_api(series_ids):
    """Fetch from BLS API v2. Max 25 series per request without API key."""
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = json.dumps({
        "seriesid": series_ids,
        "startyear": "2024",
        "endyear": "2024",
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "User-Agent": "salary-site/1.0",
    })
    ctx = ssl.create_default_context()

    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_all():
    """Build all series IDs and fetch in batches."""

    # Build all series IDs we need
    all_series = {}
    for area_code in TOP_METROS:
        for occ_code in TOP_OCCUPATIONS:
            for dtype_code in WAGE_TYPES:
                sid = build_series_id(area_code, occ_code, dtype_code)
                all_series[sid] = {
                    "area_code": area_code,
                    "occ_code": occ_code,
                    "dtype_code": dtype_code,
                }

    total = len(all_series)
    batch_size = 25  # BLS limit without API key
    daily_limit = 25  # requests per day without key
    series_list = list(all_series.keys())

    print(f"Total series needed: {total}")
    print(f"Batches of {batch_size}: {total // batch_size + 1}")
    print(f"Daily API limit (no key): {daily_limit} requests")
    print(f"With API key: 500 requests/day, 50 series/request")
    print()

    # Check for existing progress
    progress_file = os.path.join(DATA_DIR, "fetch_progress.json")
    results = {}
    start_batch = 0

    if os.path.exists(progress_file):
        with open(progress_file) as f:
            saved = json.load(f)
            results = saved.get("results", {})
            start_batch = saved.get("next_batch", 0)
        print(f"Resuming from batch {start_batch} ({len(results)} results so far)")

    # Fetch in batches
    batches = [series_list[i:i+batch_size] for i in range(0, total, batch_size)]
    requests_made = 0

    for batch_num, batch in enumerate(batches):
        if batch_num < start_batch:
            continue

        if requests_made >= daily_limit:
            print(f"\nHit daily limit ({daily_limit} requests). Saving progress...")
            save_progress(progress_file, results, batch_num)
            print(f"Run again tomorrow to continue (or register for a free BLS API key).")
            break

        print(f"Batch {batch_num + 1}/{len(batches)} ({len(batch)} series)...", end=" ")

        try:
            response = fetch_api(batch)
            requests_made += 1

            if response.get("status") == "REQUEST_SUCCEEDED":
                for series in response["Results"]["series"]:
                    sid = series["seriesID"]
                    if series["data"]:
                        value = series["data"][0]["value"]
                        meta = all_series[sid]
                        key = f"{meta['area_code']}_{meta['occ_code']}_{meta['dtype_code']}"
                        results[key] = {
                            "series_id": sid,
                            "area_code": meta["area_code"],
                            "occ_code": meta["occ_code"],
                            "dtype": WAGE_TYPES[meta["dtype_code"]],
                            "value": value,
                        }
                print(f"OK ({len(results)} total results)")
            else:
                print(f"FAILED: {response.get('message', 'Unknown error')}")

            time.sleep(0.5)  # Be nice to the API

        except Exception as e:
            print(f"ERROR: {e}")
            save_progress(progress_file, results, batch_num)
            break

    else:
        # All batches complete
        print(f"\nAll batches complete! {len(results)} data points collected.")
        if os.path.exists(progress_file):
            os.remove(progress_file)

    return results


def save_progress(filepath, results, next_batch):
    """Save fetch progress for resuming."""
    with open(filepath, "w") as f:
        json.dump({"results": results, "next_batch": next_batch}, f)
    print(f"Progress saved ({len(results)} results, resume at batch {next_batch})")


def build_salary_records(raw_results):
    """Convert raw API results into structured salary records per metro/occupation."""
    records = {}

    for key, item in raw_results.items():
        area = item["area_code"]
        occ = item["occ_code"]
        record_key = f"{area}_{occ}"

        if record_key not in records:
            records[record_key] = {
                "area_code": area,
                "area_name": TOP_METROS.get(area, "Unknown"),
                "occ_code": occ,
                "occ_name": TOP_OCCUPATIONS.get(occ, "Unknown"),
            }

        try:
            records[record_key][item["dtype"]] = float(item["value"])
        except (ValueError, TypeError):
            records[record_key][item["dtype"]] = None

    return list(records.values())


def main():
    print("=== BLS Salary Data Fetcher ===\n")
    print(f"Metros: {len(TOP_METROS)}")
    print(f"Occupations: {len(TOP_OCCUPATIONS)}")
    print(f"Potential salary pages: {len(TOP_METROS) * len(TOP_OCCUPATIONS)}")
    print()

    raw = fetch_all()

    if raw:
        records = build_salary_records(raw)
        output_path = os.path.join(DATA_DIR, "salary_data.json")
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)
        print(f"\nSaved {len(records)} salary records to {output_path}")

        # Also save reference data
        ref = {"metros": TOP_METROS, "occupations": TOP_OCCUPATIONS}
        ref_path = os.path.join(DATA_DIR, "reference_data.json")
        with open(ref_path, "w") as f:
            json.dump(ref, f, indent=2)
        print(f"Saved reference data to {ref_path}")

        # Show sample
        print("\n--- Sample Records ---")
        for r in records[:3]:
            print(f"  {r['occ_name']} in {r['area_name']}")
            if r.get('median_annual'):
                print(f"    Median: ${r['median_annual']:,.0f}")
            if r.get('mean_annual'):
                print(f"    Mean:   ${r['mean_annual']:,.0f}")


if __name__ == "__main__":
    main()
