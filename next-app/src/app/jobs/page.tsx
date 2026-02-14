import Link from "next/link";
import { Metadata } from "next";
import { getUniqueOccupations, getSalariesByOccupation, formatSalary } from "@/lib/data";

export const metadata: Metadata = {
  title: "Browse Jobs - Salary Data by Occupation",
  description: "Explore salary data for 60+ occupations across the US. See median pay, salary ranges, and compare cities for every job title.",
};

export default function JobsPage() {
  const occupations = getUniqueOccupations();

  const occWithStats = occupations.map((occ) => {
    const records = getSalariesByOccupation(occ.slug);
    const medians = records.map((r) => r.median_annual);
    const avgMedian = Math.round(medians.reduce((a, b) => a + b, 0) / medians.length);
    return { ...occ, avgMedian, cityCount: records.length };
  }).sort((a, b) => b.avgMedian - a.avgMedian);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Browse Jobs</h1>
      <p className="text-gray-600 mb-8">Salary data for {occupations.length} occupations</p>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left py-3 px-4 font-medium text-gray-600">Job Title</th>
              <th className="text-right py-3 px-4 font-medium text-gray-600">Avg Median Salary</th>
              <th className="text-right py-3 px-4 font-medium text-gray-600">Cities</th>
            </tr>
          </thead>
          <tbody>
            {occWithStats.map((occ) => (
              <tr key={occ.slug} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <Link href={`/jobs/${occ.slug}`} className="text-blue-600 hover:underline font-medium">
                    {occ.name}
                  </Link>
                </td>
                <td className="text-right py-3 px-4 font-medium">
                  {formatSalary(occ.avgMedian)}
                </td>
                <td className="text-right py-3 px-4 text-gray-600">
                  {occ.cityCount}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
