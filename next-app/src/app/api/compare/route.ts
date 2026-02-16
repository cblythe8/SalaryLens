import { NextRequest } from "next/server";
import { getSalariesByCity } from "@/lib/data";

export async function GET(req: NextRequest) {
  const citySlugs = req.nextUrl.searchParams.get("cities")?.split(",").filter(Boolean) || [];

  if (citySlugs.length < 2) {
    return Response.json({ error: "At least 2 cities required" }, { status: 400 });
  }

  // Get records for each city
  const cityRecords = citySlugs.map((slug) => ({
    slug,
    records: getSalariesByCity(slug),
  }));

  // Find the city info (name, state, currency) from first record
  const cities = cityRecords.map((c) => ({
    slug: c.slug,
    name: c.records[0]?.city_short || c.slug,
    state: c.records[0]?.state || "",
    currency: c.records[0]?.currency || "USD",
  }));

  // Build occupation maps per city
  const occMaps = cityRecords.map((c) =>
    new Map(c.records.map((r) => [r.occ_slug, r]))
  );

  // Find common occupations (present in ALL selected cities)
  const firstMap = occMaps[0];
  const commonSlugs = [...firstMap.keys()].filter((slug) =>
    occMaps.every((m) => m.has(slug))
  );

  // Build comparison data sorted by first city's median
  const comparisons = commonSlugs
    .map((occSlug) => ({
      occSlug,
      occName: firstMap.get(occSlug)!.occ_name,
      salaries: occMaps.map((m) => ({
        median: m.get(occSlug)!.median_annual,
        currency: m.get(occSlug)!.currency,
      })),
    }))
    .sort((a, b) => b.salaries[0].median - a.salaries[0].median);

  return Response.json({ cities, comparisons });
}
