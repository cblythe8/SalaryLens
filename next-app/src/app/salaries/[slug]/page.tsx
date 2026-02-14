import { notFound } from "next/navigation";
import Link from "next/link";
import { Metadata } from "next";
import {
  getSalaryBySlug,
  getSalariesByOccupation,
  getOccupationContent,
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
  const record = getSalaryBySlug(slug);
  if (!record) return {};

  return {
    title: `${record.occ_name} Salary in ${record.city_short}, ${record.state}`,
    description: `The average ${record.occ_name} in ${record.city_short} makes ${formatSalary(record.median_annual, record.currency)} per year. See full salary range from ${formatSalary(record.pct10_annual, record.currency)} to ${formatSalary(record.pct90_annual, record.currency)}.`,
  };
}

export default async function SalaryPage({ params }: PageProps) {
  const { slug } = await params;
  const record = getSalaryBySlug(slug);

  if (!record) notFound();

  const occContent = getOccupationContent(record.occ_slug);
  const citySlugForContent = record.city_short.toLowerCase().replace(/\s+/g, "-");
  const cityContentData = getCityContent(citySlugForContent);

  // Get same occupation in other cities for comparison
  const otherCities = getSalariesByOccupation(record.occ_slug)
    .filter((r) => r.area_code !== record.area_code)
    .sort((a, b) => b.median_annual - a.median_annual);

  // Calculate salary bar percentages (for visual range display)
  const maxSalary = record.pct90_annual;
  const barWidth = (val: number) => Math.round((val / maxSalary) * 100);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Home</Link>
        {" / "}
        <Link href={`/jobs/${record.occ_slug}`} className="hover:text-blue-600">
          {record.occ_name}
        </Link>
        {" / "}
        <span className="text-gray-900">{record.city_short}</span>
      </nav>

      {/* Title */}
      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        {record.occ_name} Salary in {record.city_short}, {record.state}
      </h1>
      <p className="text-gray-500 mb-8">
        Updated 2024 &middot; Source: {record.country === "CA" ? "Statistics Canada" : "U.S. Bureau of Labor Statistics"}
        {record.currency === "CAD" && <span className="ml-2 text-xs bg-gray-100 px-2 py-0.5 rounded">CAD</span>}
      </p>

      {/* Key Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Median Salary</p>
          <p className="text-2xl font-bold text-blue-600">
            {formatSalary(record.median_annual, record.currency)}
          </p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Average Salary</p>
          <p className="text-2xl font-bold">{formatSalary(record.mean_annual, record.currency)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Salary Range</p>
          <p className="text-lg font-semibold">
            {formatSalary(record.pct10_annual, record.currency)} - {formatSalary(record.pct90_annual, record.currency)}
          </p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">Employed</p>
          <p className="text-2xl font-bold">{formatNumber(record.employment)}</p>
        </div>
      </div>

      {/* Salary Range Visualization */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
        <h2 className="text-xl font-bold mb-6">Salary Distribution</h2>
        <div className="space-y-4">
          {[
            { label: "Top 10%", value: record.pct90_annual, color: "bg-green-500" },
            { label: "75th Percentile", value: record.pct75_annual, color: "bg-green-400" },
            { label: "Median", value: record.median_annual, color: "bg-blue-500" },
            { label: "25th Percentile", value: record.pct25_annual, color: "bg-orange-400" },
            { label: "Bottom 10%", value: record.pct10_annual, color: "bg-red-400" },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-4">
              <span className="text-sm text-gray-600 w-36 text-right">{item.label}</span>
              <div className="flex-1 bg-gray-100 rounded-full h-6 relative">
                <div
                  className={`${item.color} h-6 rounded-full flex items-center justify-end pr-2`}
                  style={{ width: `${barWidth(item.value)}%` }}
                >
                  <span className="text-xs text-white font-medium">
                    {formatSalary(item.value, record.currency)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-400 mt-4">
          10th to 90th percentile range. Half of all {record.occ_name.toLowerCase()} earn
          between {formatSalary(record.pct25_annual, record.currency)} and {formatSalary(record.pct75_annual, record.currency)}.
        </p>
      </div>

      {/* About This Role */}
      {occContent && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-3">
            About {record.occ_name} in {record.city_short}
          </h2>
          <p className="text-gray-700 leading-relaxed mb-4">{occContent.description}</p>
          {cityContentData && (
            <p className="text-gray-600 text-sm">
              In {record.city_short}, {record.occ_name.toLowerCase()} benefit from {
                cityContentData.cost_of_living === "high"
                  ? "higher salaries that reflect the area's elevated cost of living"
                  : cityContentData.cost_of_living === "low"
                  ? "a lower cost of living that stretches their salary further"
                  : "a moderate cost of living that balances earnings with expenses"
              }.
              {cityContentData.top_industries.length > 0 && ` The area's major industries include ${cityContentData.top_industries.slice(0, 3).join(", ")}.`}
            </p>
          )}
        </div>
      )}

      {/* Key Skills + Education */}
      {occContent && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-bold mb-3">Key Skills</h3>
            <div className="flex flex-wrap gap-2">
              {occContent.skills.map((skill) => (
                <span key={skill} className="bg-blue-50 text-blue-700 px-2.5 py-1 rounded-full text-xs font-medium">
                  {skill}
                </span>
              ))}
            </div>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-bold mb-2">Education</h3>
            <p className="text-blue-600 text-sm font-medium mb-1">{occContent.education}</p>
            <p className="text-gray-600 text-xs">{occContent.education_detail}</p>
          </div>
        </div>
      )}

      {/* Salary Tips */}
      {occContent?.salary_tips && (
        <div className="bg-blue-50 rounded-lg border border-blue-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-4">Tips to Earn More as a {record.occ_name}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {occContent.salary_tips.map((tip, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="text-blue-500 font-bold text-sm mt-0.5">{i + 1}.</span>
                <span className="text-gray-700 text-sm">{tip}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Compare Other Cities */}
      {otherCities.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-4">
            {record.occ_name} Salary in Other Cities
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 font-medium text-gray-500">City</th>
                  <th className="text-right py-3 font-medium text-gray-500">Median</th>
                  <th className="text-right py-3 font-medium text-gray-500">Range</th>
                  <th className="text-right py-3 font-medium text-gray-500">vs {record.city_short}</th>
                </tr>
              </thead>
              <tbody>
                {otherCities.map((city) => {
                  const diff = city.median_annual - record.median_annual;
                  const diffPct = Math.round((diff / record.median_annual) * 100);
                  const citySlug = city.city_short.toLowerCase().replace(/\s+/g, "-");
                  return (
                    <tr key={city.area_code} className="border-b border-gray-100">
                      <td className="py-3">
                        <Link
                          href={`/salaries/${city.occ_slug}-in-${citySlug}`}
                          className="text-blue-600 hover:underline"
                        >
                          {city.city_short}, {city.state}
                        </Link>
                      </td>
                      <td className="text-right py-3 font-medium">
                        {formatSalary(city.median_annual, city.currency)}
                      </td>
                      <td className="text-right py-3 text-gray-500">
                        {formatSalary(city.pct10_annual, city.currency)} - {formatSalary(city.pct90_annual, city.currency)}
                      </td>
                      <td className={`text-right py-3 font-medium ${diff > 0 ? "text-green-600" : "text-red-600"}`}>
                        {diff > 0 ? "+" : ""}{diffPct}%
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* JSON-LD Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "OccupationalExperienceRequirements",
            name: record.occ_name,
            occupationalCategory: record.occ_code,
            estimatedSalary: {
              "@type": "MonetaryAmountDistribution",
              name: "base",
              currency: record.currency,
              median: record.median_annual,
              percentile10: record.pct10_annual,
              percentile25: record.pct25_annual,
              percentile75: record.pct75_annual,
              percentile90: record.pct90_annual,
            },
          }),
        }}
      />
    </div>
  );
}
