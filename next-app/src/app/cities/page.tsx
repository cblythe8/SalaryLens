import Link from "next/link";
import { Metadata } from "next";
import { getUniqueCities, getSalariesByCity, formatSalary } from "@/lib/data";

export const metadata: Metadata = {
  title: "Browse Cities - Salary Data by Location",
  description: "Compare salaries across 50+ US metro areas. Find the highest paying cities for your occupation.",
};

export default function CitiesPage() {
  const cities = getUniqueCities();

  const cityWithStats = cities.map((city) => {
    const records = getSalariesByCity(city.slug);
    const medians = records.map((r) => r.median_annual);
    const avgMedian = Math.round(medians.reduce((a, b) => a + b, 0) / medians.length);
    const topJob = [...records].sort((a, b) => b.median_annual - a.median_annual)[0];
    return { ...city, avgMedian, jobCount: records.length, topJob: topJob?.occ_name };
  }).sort((a, b) => b.avgMedian - a.avgMedian);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Browse Cities</h1>
      <p className="text-gray-600 mb-8">Salary data across {cities.length} US metro areas</p>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left py-3 px-4 font-medium text-gray-600">City</th>
              <th className="text-right py-3 px-4 font-medium text-gray-600">Avg Median Salary</th>
              <th className="text-left py-3 px-4 font-medium text-gray-600">Top Paying Job</th>
              <th className="text-right py-3 px-4 font-medium text-gray-600">Jobs Tracked</th>
            </tr>
          </thead>
          <tbody>
            {cityWithStats.map((city) => (
              <tr key={city.slug} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <Link href={`/cities/${city.slug}`} className="text-blue-600 hover:underline font-medium">
                    {city.name}, {city.state}
                  </Link>
                </td>
                <td className="text-right py-3 px-4 font-medium">
                  {formatSalary(city.avgMedian)}
                </td>
                <td className="py-3 px-4 text-gray-600">
                  {city.topJob}
                </td>
                <td className="text-right py-3 px-4 text-gray-600">
                  {city.jobCount}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
