import { NextRequest, NextResponse } from "next/server";
import {
  getAllSalaryRecords,
  getUniqueOccupations,
  getUniqueCities,
  formatSalary,
} from "@/lib/data";

interface SearchResult {
  label: string;
  sublabel: string;
  href: string;
  type: "salary" | "job" | "city";
}

export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams.get("q")?.toLowerCase() || "";

  if (query.length < 2) {
    return NextResponse.json([]);
  }

  const results: SearchResult[] = [];
  const limit = 8;

  // Search jobs first (highest priority)
  const occupations = getUniqueOccupations();
  for (const occ of occupations) {
    if (results.length >= limit) break;
    if (occ.name.toLowerCase().includes(query)) {
      results.push({
        label: occ.name,
        sublabel: "View salary across all cities",
        href: `/jobs/${occ.slug}`,
        type: "job",
      });
    }
  }

  // Search cities
  const cities = getUniqueCities();
  for (const city of cities) {
    if (results.length >= limit) break;
    const cityText = `${city.name}, ${city.state}`.toLowerCase();
    if (cityText.includes(query) || city.name.toLowerCase().includes(query)) {
      results.push({
        label: `${city.name}, ${city.state}`,
        sublabel: "View all salaries in this city",
        href: `/cities/${city.slug}`,
        type: "city",
      });
    }
  }

  // Search salary pages (job + city combos)
  if (results.length < limit) {
    const records = getAllSalaryRecords();
    for (const r of records) {
      if (results.length >= limit) break;
      const text = `${r.occ_name} in ${r.city_short}`.toLowerCase();
      if (text.includes(query)) {
        const citySlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
        results.push({
          label: `${r.occ_name} in ${r.city_short}`,
          sublabel: `Median: ${formatSalary(r.median_annual, r.currency)}`,
          href: `/salaries/${r.occ_slug}-in-${citySlug}`,
          type: "salary",
        });
      }
    }
  }

  return NextResponse.json(results);
}
