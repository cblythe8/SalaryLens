import Link from "next/link";
import { Metadata } from "next";
import {
  getTopPayingRecords,
  getUniqueOccupations,
  getUniqueCities,
  formatSalary,
} from "@/lib/data";

export const metadata: Metadata = {
  title: "Salary Data - Browse by Job or City",
  description:
    "Browse salary data for 489 occupations across 60 cities in the US and Canada. Find median pay, salary ranges, and more.",
};

export default function SalariesPage() {
  const topPaying = getTopPayingRecords(50);
  const occupations = getUniqueOccupations();
  const cities = getUniqueCities();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Salary Data</h1>
      <p className="text-gray-800 mb-8">
        {occupations.length} occupations across {cities.length} cities in the US
        and Canada
      </p>

      {/* Top 50 highest paying */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Top 50 Highest Paying</h2>
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left py-3 px-4 font-medium text-gray-800">
                  Job Title
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-800">
                  City
                </th>
                <th className="text-right py-3 px-4 font-medium text-gray-800">
                  Median
                </th>
                <th className="text-right py-3 px-4 font-medium text-gray-800">
                  Range
                </th>
              </tr>
            </thead>
            <tbody>
              {topPaying.map((r) => {
                const citySlug = r.city_short
                  .toLowerCase()
                  .replace(/\s+/g, "-");
                const slug = `${r.occ_slug}-in-${citySlug}`;
                return (
                  <tr
                    key={slug}
                    className="border-b border-gray-100 hover:bg-gray-50"
                  >
                    <td className="py-3 px-4">
                      <Link
                        href={`/salaries/${slug}`}
                        className="text-blue-600 hover:underline font-medium"
                      >
                        {r.occ_name}
                      </Link>
                    </td>
                    <td className="py-3 px-4 text-gray-800">
                      {r.city_short}, {r.state}
                    </td>
                    <td className="text-right py-3 px-4 font-medium">
                      {formatSalary(r.median_annual, r.currency)}
                    </td>
                    <td className="text-right py-3 px-4 text-gray-800">
                      {formatSalary(r.pct10_annual, r.currency)} &ndash;{" "}
                      {formatSalary(r.pct90_annual, r.currency)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* Browse by Job */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Browse by Job Title</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {occupations.map((occ) => (
            <Link
              key={occ.slug}
              href={`/jobs/${occ.slug}`}
              className="text-sm text-gray-700 hover:text-blue-600 hover:underline py-1"
            >
              {occ.name}
            </Link>
          ))}
        </div>
      </section>

      {/* Browse by City */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Browse by City</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {cities.map((city) => (
            <Link
              key={city.slug}
              href={`/cities/${city.slug}`}
              className="text-sm text-gray-700 hover:text-blue-600 hover:underline py-1"
            >
              {city.name}, {city.state}
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
