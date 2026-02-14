import Link from "next/link";
import { Metadata } from "next";
import { getUniqueCities, getSalariesByCity, formatSalary } from "@/lib/data";

export const metadata: Metadata = {
  title: "Compare City Salaries - Side by Side",
  description:
    "Compare salaries between cities. See which city pays more for your job title.",
};

export default function ComparePage() {
  const cities = getUniqueCities();

  // Build city stats for display
  const cityStats = cities.map((city) => {
    const records = getSalariesByCity(city.slug);
    const avgMedian =
      records.length > 0
        ? Math.round(records.reduce((s, r) => s + r.median_annual, 0) / records.length)
        : 0;
    const currency = records.length > 0 ? records[0].currency : "USD";
    return { ...city, avgMedian, currency, jobCount: records.length };
  });

  // Generate popular comparisons (top 5 US cities paired up, plus some cross-border)
  const popularPairs = [
    ["new-york", "san-francisco"],
    ["new-york", "toronto"],
    ["san-francisco", "seattle"],
    ["toronto", "vancouver"],
    ["chicago", "austin"],
    ["boston", "washington-dc"],
    ["los-angeles", "miami"],
    ["new-york", "los-angeles"],
    ["vancouver", "calgary"],
    ["seattle", "denver"],
  ].filter(([a, b]) => {
    return cities.some((c) => c.slug === a) && cities.some((c) => c.slug === b);
  });

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Compare City Salaries</h1>
      <p className="text-gray-800 mb-8">
        See how salaries stack up across different cities
      </p>

      {/* Popular Comparisons */}
      <div className="mb-10">
        <h2 className="text-xl font-bold mb-4">Popular Comparisons</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {popularPairs.map(([a, b]) => {
            const cityA = cityStats.find((c) => c.slug === a);
            const cityB = cityStats.find((c) => c.slug === b);
            if (!cityA || !cityB) return null;
            return (
              <Link
                key={`${a}-vs-${b}`}
                href={`/compare/${a}-vs-${b}`}
                className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-900">
                      {cityA.name}, {cityA.state}
                    </p>
                    <p className="text-sm text-blue-600">
                      Avg: {formatSalary(cityA.avgMedian, cityA.currency)}
                    </p>
                  </div>
                  <span className="text-gray-800 font-bold text-sm mx-3">VS</span>
                  <div className="text-right">
                    <p className="font-semibold text-gray-900">
                      {cityB.name}, {cityB.state}
                    </p>
                    <p className="text-sm text-purple-600">
                      Avg: {formatSalary(cityB.avgMedian, cityB.currency)}
                    </p>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* All Cities Grid */}
      <div>
        <h2 className="text-xl font-bold mb-4">Browse All Cities</h2>
        <p className="text-sm text-gray-800 mb-4">
          Pick any two cities to compare. Click a city to see its full salary data.
        </p>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {cityStats.map((city) => (
            <Link
              key={city.slug}
              href={`/cities/${city.slug}`}
              className="bg-white rounded-lg border border-gray-200 px-4 py-3 hover:border-blue-300 hover:shadow-sm transition-all"
            >
              <p className="text-sm font-medium text-gray-900">
                {city.name}, {city.state}
              </p>
              <p className="text-xs text-gray-800">
                Avg: {formatSalary(city.avgMedian, city.currency)} &middot; {city.jobCount} jobs
              </p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
