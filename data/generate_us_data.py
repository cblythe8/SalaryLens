"""
Generate realistic US salary data based on published BLS OES ranges.
Uses national medians and applies metro-area adjustment factors.

This creates sample data good enough for the MVP. Once we get a BLS API key,
we can replace it with real data using build_from_api.py.
"""

import json
import os
import random

random.seed(42)  # Reproducible results

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "next-app", "src", "lib")

# National median salaries (approximate, from BLS OES 2023)
OCCUPATIONS = {
    "software-developers": {"code": "15-1252", "name": "Software Developers", "nat_median": 132270},
    "data-scientists": {"code": "15-2051", "name": "Data Scientists", "nat_median": 108020},
    "registered-nurses": {"code": "29-1141", "name": "Registered Nurses", "nat_median": 86070},
    "accountants-and-auditors": {"code": "13-2011", "name": "Accountants and Auditors", "nat_median": 79880},
    "financial-analysts": {"code": "13-2051", "name": "Financial Analysts", "nat_median": 99890},
    "marketing-managers": {"code": "11-2021", "name": "Marketing Managers", "nat_median": 156580},
    "product-managers": {"code": "15-1299", "name": "Product Managers", "nat_median": 120990},
    "web-developers": {"code": "15-1254", "name": "Web Developers", "nat_median": 80730},
    "cybersecurity-analysts": {"code": "15-1212", "name": "Information Security Analysts", "nat_median": 120360},
    "mechanical-engineers": {"code": "17-2141", "name": "Mechanical Engineers", "nat_median": 96310},
    "lawyers": {"code": "23-1011", "name": "Lawyers", "nat_median": 145760},
    "data-analysts": {"code": "15-1211", "name": "Computer Systems Analysts", "nat_median": 103800},
    "operations-managers": {"code": "11-1021", "name": "General and Operations Managers", "nat_median": 101280},
    "it-managers": {"code": "11-3021", "name": "IT Managers", "nat_median": 169510},
    "financial-managers": {"code": "11-3031", "name": "Financial Managers", "nat_median": 156100},
    "nurse-practitioners": {"code": "29-1171", "name": "Nurse Practitioners", "nat_median": 126260},
    "physician-assistants": {"code": "29-1071", "name": "Physician Assistants", "nat_median": 130020},
    "elementary-school-teachers": {"code": "25-2021", "name": "Elementary School Teachers", "nat_median": 61690},
    "electricians": {"code": "47-2111", "name": "Electricians", "nat_median": 61590},
    "police-officers": {"code": "33-3051", "name": "Police Officers", "nat_median": 74910},
    "graphic-designers": {"code": "27-1024", "name": "Graphic Designers", "nat_median": 57990},
    "hr-specialists": {"code": "13-1071", "name": "Human Resources Specialists", "nat_median": 67650},
    "civil-engineers": {"code": "17-2051", "name": "Civil Engineers", "nat_median": 89940},
    "electrical-engineers": {"code": "17-2071", "name": "Electrical Engineers", "nat_median": 109350},
    "pharmacists": {"code": "29-1051", "name": "Pharmacists", "nat_median": 136030},
    "truck-drivers": {"code": "53-3032", "name": "Truck Drivers", "nat_median": 54320},
    "plumbers": {"code": "47-2152", "name": "Plumbers", "nat_median": 61550},
    "hvac-technicians": {"code": "49-9021", "name": "HVAC Technicians", "nat_median": 57300},
    "customer-service-reps": {"code": "43-4051", "name": "Customer Service Representatives", "nat_median": 39680},
    "management-consultants": {"code": "13-1111", "name": "Management Consultants", "nat_median": 99410},
}

# Metro areas with cost-of-living adjustment factors
METROS = {
    "new-york": {"code": "35620", "name": "New York-Newark-Jersey City, NY-NJ-PA", "short": "New York", "state": "NY", "factor": 1.25, "emp_mult": 1.8},
    "los-angeles": {"code": "31080", "name": "Los Angeles-Long Beach-Anaheim, CA", "short": "Los Angeles", "state": "CA", "factor": 1.18, "emp_mult": 1.4},
    "san-francisco": {"code": "41860", "name": "San Francisco-Oakland-Berkeley, CA", "short": "San Francisco", "state": "CA", "factor": 1.38, "emp_mult": 0.9},
    "seattle": {"code": "42660", "name": "Seattle-Tacoma-Bellevue, WA", "short": "Seattle", "state": "WA", "factor": 1.30, "emp_mult": 1.0},
    "chicago": {"code": "16980", "name": "Chicago-Naperville-Elgin, IL-IN-WI", "short": "Chicago", "state": "IL", "factor": 1.05, "emp_mult": 1.3},
    "washington-dc": {"code": "47900", "name": "Washington-Arlington-Alexandria, DC-VA-MD-WV", "short": "Washington DC", "state": "DC", "factor": 1.22, "emp_mult": 1.2},
    "boston": {"code": "14460", "name": "Boston-Cambridge-Nashua, MA-NH", "short": "Boston", "state": "MA", "factor": 1.24, "emp_mult": 0.9},
    "austin": {"code": "12420", "name": "Austin-Round Rock-Georgetown, TX", "short": "Austin", "state": "TX", "factor": 1.10, "emp_mult": 0.6},
    "dallas": {"code": "19100", "name": "Dallas-Fort Worth-Arlington, TX", "short": "Dallas", "state": "TX", "factor": 1.05, "emp_mult": 1.1},
    "denver": {"code": "19740", "name": "Denver-Aurora-Lakewood, CO", "short": "Denver", "state": "CO", "factor": 1.12, "emp_mult": 0.7},
    "atlanta": {"code": "12060", "name": "Atlanta-Sandy Springs-Alpharetta, GA", "short": "Atlanta", "state": "GA", "factor": 1.02, "emp_mult": 0.9},
    "miami": {"code": "33100", "name": "Miami-Fort Lauderdale-Pompano Beach, FL", "short": "Miami", "state": "FL", "factor": 0.95, "emp_mult": 0.7},
    "san-jose": {"code": "41940", "name": "San Jose-Sunnyvale-Santa Clara, CA", "short": "San Jose", "state": "CA", "factor": 1.42, "emp_mult": 0.5},
    "phoenix": {"code": "38060", "name": "Phoenix-Mesa-Chandler, AZ", "short": "Phoenix", "state": "AZ", "factor": 0.98, "emp_mult": 0.8},
    "minneapolis": {"code": "33460", "name": "Minneapolis-St. Paul-Bloomington, MN-WI", "short": "Minneapolis", "state": "MN", "factor": 1.08, "emp_mult": 0.7},
    "philadelphia": {"code": "37980", "name": "Philadelphia-Camden-Wilmington, PA-NJ-DE-MD", "short": "Philadelphia", "state": "PA", "factor": 1.08, "emp_mult": 1.0},
    "san-diego": {"code": "41740", "name": "San Diego-Chula Vista-Carlsbad, CA", "short": "San Diego", "state": "CA", "factor": 1.15, "emp_mult": 0.6},
    "nashville": {"code": "34980", "name": "Nashville-Davidson-Murfreesboro-Franklin, TN", "short": "Nashville", "state": "TN", "factor": 0.98, "emp_mult": 0.5},
    "portland": {"code": "38900", "name": "Portland-Vancouver-Hillsboro, OR-WA", "short": "Portland", "state": "OR", "factor": 1.10, "emp_mult": 0.5},
    "raleigh": {"code": "39580", "name": "Raleigh-Cary, NC", "short": "Raleigh", "state": "NC", "factor": 1.02, "emp_mult": 0.4},
    "charlotte": {"code": "16740", "name": "Charlotte-Concord-Gastonia, NC-SC", "short": "Charlotte", "state": "NC", "factor": 0.98, "emp_mult": 0.5},
    "salt-lake-city": {"code": "41620", "name": "Salt Lake City, UT", "short": "Salt Lake City", "state": "UT", "factor": 1.00, "emp_mult": 0.4},
    "houston": {"code": "26420", "name": "Houston-The Woodlands-Sugar Land, TX", "short": "Houston", "state": "TX", "factor": 1.02, "emp_mult": 1.1},
    "las-vegas": {"code": "29820", "name": "Las Vegas-Henderson-Paradise, NV", "short": "Las Vegas", "state": "NV", "factor": 0.95, "emp_mult": 0.4},
    "detroit": {"code": "19820", "name": "Detroit-Warren-Dearborn, MI", "short": "Detroit", "state": "MI", "factor": 0.98, "emp_mult": 0.7},
}


def generate_record(occ_slug, occ_info, metro_slug, metro_info):
    """Generate a salary record with realistic spreads."""
    nat_med = occ_info["nat_median"]
    factor = metro_info["factor"]

    # Add some randomness to the factor (±3%)
    adjusted_factor = factor * random.uniform(0.97, 1.03)

    median = round(nat_med * adjusted_factor / 1000) * 1000
    mean = round(median * random.uniform(1.02, 1.12) / 1000) * 1000

    # Percentile spreads vary by occupation type
    # Higher-paid jobs tend to have wider spreads
    if median > 120000:
        spread = 0.45
    elif median > 80000:
        spread = 0.40
    else:
        spread = 0.35

    p10 = round(median * (1 - spread) / 1000) * 1000
    p25 = round(median * (1 - spread * 0.55) / 1000) * 1000
    p75 = round(median * (1 + spread * 0.45) / 1000) * 1000
    p90 = round(median * (1 + spread * 0.75) / 1000) * 1000

    # Employment based on national employment scaled by metro size
    base_emp = random.randint(2000, 25000)
    emp = round(base_emp * metro_info["emp_mult"] / 100) * 100
    emp = max(emp, 500)

    return {
        "area_code": metro_info["code"],
        "area_name": metro_info["name"],
        "city_short": metro_info["short"],
        "state": metro_info["state"],
        "country": "US",
        "currency": "USD",
        "occ_code": occ_info["code"],
        "occ_name": occ_info["name"],
        "occ_slug": occ_slug,
        "employment": emp,
        "mean_annual": mean,
        "median_annual": median,
        "pct10_annual": p10,
        "pct25_annual": p25,
        "pct75_annual": p75,
        "pct90_annual": p90,
    }


def main():
    print("Generating US salary data...")

    us_records = []
    for occ_slug, occ_info in OCCUPATIONS.items():
        for metro_slug, metro_info in METROS.items():
            record = generate_record(occ_slug, occ_info, metro_slug, metro_info)
            us_records.append(record)

    print(f"  Generated {len(us_records)} US records")

    # Load existing Canadian data
    ca_path = os.path.join(OUTPUT_DIR, "salary_data.json")
    ca_records = []
    if os.path.exists(ca_path):
        with open(ca_path) as f:
            existing = json.load(f)
            ca_records = [r for r in existing if r.get("country") == "CA"]
        print(f"  Preserved {len(ca_records)} Canadian records")

    # Combine and sort
    all_records = us_records + ca_records
    all_records.sort(key=lambda r: r["median_annual"], reverse=True)

    # Write
    with open(ca_path, "w") as f:
        json.dump(all_records, f, indent=2)

    occupations = set(r["occ_slug"] for r in all_records)
    us_cities = set(r["city_short"] for r in all_records if r["country"] == "US")
    ca_cities = set(r["city_short"] for r in all_records if r["country"] == "CA")

    print(f"\n{'=' * 50}")
    print(f"  Total records: {len(all_records)}")
    print(f"  Occupations: {len(occupations)}")
    print(f"  US Cities: {len(us_cities)}")
    print(f"  CA Cities: {len(ca_cities)}")
    print(f"  Total pages: ~{len(all_records)}")
    print(f"{'=' * 50}")

    print(f"\nTop 10 highest paying:")
    for r in all_records[:10]:
        print(f"  ${r['median_annual']:>9,} {r['currency']}  {r['occ_name']} in {r['city_short']}")

    print(f"\nBottom 5:")
    for r in all_records[-5:]:
        print(f"  ${r['median_annual']:>9,} {r['currency']}  {r['occ_name']} in {r['city_short']}")


if __name__ == "__main__":
    main()
