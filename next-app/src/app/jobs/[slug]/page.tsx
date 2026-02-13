import { notFound } from "next/navigation";
import Link from "next/link";
import { Metadata } from "next";
import {
  getUniqueOccupations,
  getSalariesByOccupation,
  formatSalary,
  formatNumber,
} from "@/lib/data";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const records = getSalariesByOccupation(slug);
  if (records.length === 0) return {};
  const name = records[0].occ_name;

  const salaries = records.map((r) => r.median_annual).sort((a, b) => a - b);
  const low = formatSalary(salaries[0]);
  const high = formatSalary(salaries[salaries.length - 1]);

  return {
    title: `${name} Salary - How Much Do ${name} Make?`,
    description: `${name} earn between ${low} and ${high} depending on location. Compare salaries across ${records.length} US cities.`,
  };
}

export default async function JobPage({ params }: PageProps) {
  const { slug } = await params;
  const records = getSalariesByOccupation(slug);

  if (records.length === 0) notFound();

  const name = records[0].occ_name;
  const sorted = [...records].sort((a, b) => b.median_annual - a.median_annual);

  const avgMedian = Math.round(
    records.reduce((sum, r) => sum + r.median_annual, 0) / records.length
  );
  const totalEmployment = records.reduce((sum, r) => sum + r.employment, 0);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Home</Link>
        {" / "}
        <Link href="/jobs" className="hover:text-blue-600">Jobs</Link>
        {" / "}
        <span className="text-gray-900">{name}</span>
      </nav>

      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        {name} Salary
      </h1>
      <p className="text-gray-500 mb-8">
        Salary data across {records.length} metro areas in the US &amp; Canada
      </p>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Avg Median Salary</p>
          <p className="text-2xl font-bold text-blue-600">{formatSalary(avgMedian)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Highest Paying City</p>
          <p className="text-lg font-bold">{sorted[0].city_short}</p>
          <p className="text-sm text-gray-500">{formatSalary(sorted[0].median_annual)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Total Employed</p>
          <p className="text-2xl font-bold">{formatNumber(totalEmployment)}</p>
        </div>
      </div>

      {/* All Cities Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-bold mb-4">{name} Salary by City</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 font-medium text-gray-500">City</th>
                <th className="text-right py-3 font-medium text-gray-500">Median</th>
                <th className="text-right py-3 font-medium text-gray-500">Average</th>
                <th className="text-right py-3 font-medium text-gray-500">Range (10th-90th)</th>
                <th className="text-right py-3 font-medium text-gray-500">Employed</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((r) => {
                const citySlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
                return (
                  <tr key={r.area_code} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3">
                      <Link
                        href={`/salaries/${r.occ_slug}-in-${citySlug}`}
                        className="text-blue-600 hover:underline"
                      >
                        {r.city_short}, {r.state}
                      </Link>
                    </td>
                    <td className="text-right py-3 font-medium">
                      {formatSalary(r.median_annual, r.currency)}
                    </td>
                    <td className="text-right py-3 text-gray-600">
                      {formatSalary(r.mean_annual, r.currency)}
                    </td>
                    <td className="text-right py-3 text-gray-500">
                      {formatSalary(r.pct10_annual, r.currency)} - {formatSalary(r.pct90_annual, r.currency)}
                    </td>
                    <td className="text-right py-3 text-gray-500">
                      {formatNumber(r.employment)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
