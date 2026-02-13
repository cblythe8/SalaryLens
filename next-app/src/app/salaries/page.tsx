import Link from "next/link";
import { Metadata } from "next";
import { getAllSalaryRecords, formatSalary } from "@/lib/data";

export const metadata: Metadata = {
  title: "All Salaries - Browse Every Job in Every City",
  description: "Browse salary data for every job title in every US metro area. Sorted by median pay.",
};

export default function SalariesPage() {
  const records = [...getAllSalaryRecords()].sort(
    (a, b) => b.median_annual - a.median_annual
  );

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">All Salaries</h1>
      <p className="text-gray-500 mb-8">{records.length} job-city combinations, sorted by median pay</p>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left py-3 px-4 font-medium text-gray-500">Job Title</th>
              <th className="text-left py-3 px-4 font-medium text-gray-500">City</th>
              <th className="text-right py-3 px-4 font-medium text-gray-500">Median</th>
              <th className="text-right py-3 px-4 font-medium text-gray-500">Range</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r) => {
              const citySlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
              const slug = `${r.occ_slug}-in-${citySlug}`;
              return (
                <tr key={slug} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <Link href={`/salaries/${slug}`} className="text-blue-600 hover:underline font-medium">
                      {r.occ_name}
                    </Link>
                  </td>
                  <td className="py-3 px-4 text-gray-600">
                    {r.city_short}, {r.state}
                  </td>
                  <td className="text-right py-3 px-4 font-medium">
                    {formatSalary(r.median_annual, r.currency)}
                  </td>
                  <td className="text-right py-3 px-4 text-gray-500">
                    {formatSalary(r.pct10_annual, r.currency)} - {formatSalary(r.pct90_annual, r.currency)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
