import { notFound } from "next/navigation";
import Link from "next/link";
import { Metadata } from "next";
import {
  getUniqueCities,
  getSalariesByCity,
  getCityContent,
  formatSalary,
  formatNumber,
} from "@/lib/data";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const records = getSalariesByCity(slug);
  if (records.length === 0) return {};

  const city = records[0];
  const sorted = [...records].sort((a, b) => b.median_annual - a.median_annual);

  return {
    title: `Best Paying Jobs in ${city.city_short}, ${city.state}`,
    description: `Top paying jobs in ${city.city_short}: ${sorted[0].occ_name} (${formatSalary(sorted[0].median_annual, sorted[0].currency)}), ${sorted[1]?.occ_name} (${formatSalary(sorted[1]?.median_annual, sorted[1]?.currency)}), and more.`,
  };
}

export default async function CityPage({ params }: PageProps) {
  const { slug } = await params;
  const records = getSalariesByCity(slug);

  if (records.length === 0) notFound();

  const city = records[0];
  const cityContent = getCityContent(slug);
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
        <Link href="/cities" className="hover:text-blue-600">Cities</Link>
        {" / "}
        <span className="text-gray-900">{city.city_short}, {city.state}</span>
      </nav>

      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        Best Paying Jobs in {city.city_short}, {city.state}
      </h1>
      <p className="text-gray-500 mb-8">
        Salary data for {records.length} occupations in the {city.area_name} metro area
      </p>

      {/* Summary */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Avg Median Salary</p>
          <p className="text-2xl font-bold text-blue-600">{formatSalary(avgMedian, city.currency)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Top Paying Job</p>
          <p className="text-lg font-bold">{sorted[0].occ_name}</p>
          <p className="text-sm text-gray-500">{formatSalary(sorted[0].median_annual, sorted[0].currency)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Total Jobs Tracked</p>
          <p className="text-2xl font-bold">{formatNumber(totalEmployment)}</p>
        </div>
      </div>

      {/* City Overview */}
      {cityContent && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-3">Job Market in {city.city_short}</h2>
          <p className="text-gray-700 leading-relaxed">{cityContent.overview}</p>
        </div>
      )}

      {/* Top Industries + Cost of Living */}
      {cityContent && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-bold mb-3">Top Industries</h2>
            <ul className="space-y-2">
              {cityContent.top_industries.map((industry) => (
                <li key={industry} className="flex items-center gap-2 text-gray-700 text-sm">
                  <span className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0" />
                  {industry}
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-bold mb-3">Cost of Living</h2>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium mb-2 ${
              cityContent.cost_of_living === "high" ? "bg-red-100 text-red-700" :
              cityContent.cost_of_living === "low" ? "bg-green-100 text-green-700" :
              "bg-yellow-100 text-yellow-700"
            }`}>
              {cityContent.cost_of_living.charAt(0).toUpperCase() + cityContent.cost_of_living.slice(1)}
            </span>
            <p className="text-gray-600 text-sm">{cityContent.cost_of_living_detail}</p>
          </div>
        </div>
      )}

      {/* All Jobs Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-bold mb-4">All Salaries in {city.city_short}</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 font-medium text-gray-500">Job Title</th>
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
                  <tr key={r.occ_code} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3">
                      <Link
                        href={`/salaries/${r.occ_slug}-in-${citySlug}`}
                        className="text-blue-600 hover:underline"
                      >
                        {r.occ_name}
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
