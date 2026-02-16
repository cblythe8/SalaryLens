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

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <nav className="text-sm text-black mb-6">
        <Link href="/" className="hover:text-blue-600">Home</Link>
        {" / "}
        <Link href="/cities" className="hover:text-blue-600">Cities</Link>
        {" / "}
        <span className="text-black">{city.city_short}, {city.state}</span>
      </nav>

      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        Best Paying Jobs in {city.city_short}, {city.state}
      </h1>
      <p className="text-black mb-8">
        Salary data for {records.length} occupations in the {city.area_name} metro area
        <span className={`ml-2 text-xs px-2 py-0.5 rounded font-medium ${city.currency === "CAD" ? "bg-red-50 text-red-700" : "bg-blue-50 text-blue-700"}`}>
          All salaries in {city.currency === "CAD" ? "CAD $" : "USD $"}
        </span>
      </p>

      {/* Summary */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-black">Avg Median Salary</p>
          <p className="text-2xl font-bold text-blue-600">{formatSalary(avgMedian, city.currency)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-black">Top Paying Job</p>
          <p className="text-lg font-bold">{sorted[0].occ_name}</p>
          <p className="text-sm text-black">{formatSalary(sorted[0].median_annual, sorted[0].currency)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-black">Occupations Tracked</p>
          <p className="text-2xl font-bold">{records.length}</p>
        </div>
      </div>

      {/* City Overview */}
      {cityContent && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-3">Job Market in {city.city_short}</h2>
          <p className="text-black leading-relaxed">{cityContent.overview}</p>
        </div>
      )}

      {/* Top Industries + Cost of Living */}
      {cityContent && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-bold mb-3">Top Industries</h2>
            <ul className="space-y-2">
              {cityContent.top_industries.map((industry) => (
                <li key={industry} className="flex items-center gap-2 text-black text-sm">
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
            <p className="text-black text-sm">{cityContent.cost_of_living_detail}</p>
          </div>
        </div>
      )}

      {/* All Jobs Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-bold mb-4">All Salaries in {city.city_short}</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-black">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 font-medium text-black">Job Title</th>
                <th className="text-right py-3 font-medium text-black">Median</th>
                <th className="text-right py-3 font-medium text-black">Average</th>
                <th className="text-right py-3 font-medium text-black">Range (10th-90th)</th>
                <th className="text-right py-3 font-medium text-black">Est. Employed*</th>
                <th className="text-right py-3 font-medium text-black"></th>
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
                    <td className="text-right py-3 text-black">
                      {formatSalary(r.mean_annual, r.currency)}
                    </td>
                    <td className="text-right py-3 text-black">
                      {formatSalary(r.pct10_annual, r.currency)} - {formatSalary(r.pct90_annual, r.currency)}
                    </td>
                    <td className="text-right py-3 text-black">
                      {formatNumber(r.employment)}
                    </td>
                    <td className="text-right py-3">
                      <a
                        href={`https://www.indeed.com/jobs?q=${encodeURIComponent(r.occ_name)}&l=${encodeURIComponent(r.city_short + ", " + r.state)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-xs"
                      >
                        Apply
                      </a>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <p className="text-xs text-black mt-4">
          *Employment figures are estimates based on national occupational data distributed across metro areas. Actual local numbers may vary.
        </p>
      </div>
    </div>
  );
}
