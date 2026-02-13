import { notFound } from "next/navigation";
import Link from "next/link";
import { Metadata } from "next";
import {
  parseComparisonSlug,
  getSalariesByCity,
  getUniqueCities,
  formatSalary,
  formatNumber,
} from "@/lib/data";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const parsed = parseComparisonSlug(slug);
  if (!parsed) return {};

  const cities = getUniqueCities();
  const cityA = cities.find((c) => c.slug === parsed.cityA);
  const cityB = cities.find((c) => c.slug === parsed.cityB);
  if (!cityA || !cityB) return {};

  return {
    title: `${cityA.name} vs ${cityB.name} - Salary Comparison`,
    description: `Compare salaries between ${cityA.name} and ${cityB.name}. See which city pays more for top jobs like software developers, data scientists, and more.`,
  };
}

export default async function ComparePage({ params }: PageProps) {
  const { slug } = await params;
  const parsed = parseComparisonSlug(slug);
  if (!parsed) notFound();

  const cities = getUniqueCities();
  const cityAInfo = cities.find((c) => c.slug === parsed.cityA);
  const cityBInfo = cities.find((c) => c.slug === parsed.cityB);
  if (!cityAInfo || !cityBInfo) notFound();

  const recordsA = getSalariesByCity(parsed.cityA);
  const recordsB = getSalariesByCity(parsed.cityB);

  if (recordsA.length === 0 || recordsB.length === 0) notFound();

  // Find common occupations
  const occMapA = new Map(recordsA.map((r) => [r.occ_slug, r]));
  const occMapB = new Map(recordsB.map((r) => [r.occ_slug, r]));

  const commonOccs = [...occMapA.keys()].filter((k) => occMapB.has(k));

  const comparisons = commonOccs
    .map((occSlug) => ({
      occSlug,
      occName: occMapA.get(occSlug)!.occ_name,
      a: occMapA.get(occSlug)!,
      b: occMapB.get(occSlug)!,
    }))
    .sort((x, y) => y.a.median_annual - x.a.median_annual);

  // Summary stats
  const avgA =
    comparisons.length > 0
      ? Math.round(comparisons.reduce((s, c) => s + c.a.median_annual, 0) / comparisons.length)
      : 0;
  const avgB =
    comparisons.length > 0
      ? Math.round(comparisons.reduce((s, c) => s + c.b.median_annual, 0) / comparisons.length)
      : 0;

  const winsA = comparisons.filter((c) => c.a.median_annual > c.b.median_annual).length;
  const winsB = comparisons.filter((c) => c.b.median_annual > c.a.median_annual).length;

  const currencyA = recordsA[0].currency;
  const currencyB = recordsB[0].currency;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-blue-600">Home</Link>
        {" / "}
        <Link href="/compare" className="hover:text-blue-600">Compare</Link>
        {" / "}
        <span className="text-gray-900">
          {cityAInfo.name} vs {cityBInfo.name}
        </span>
      </nav>

      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        {cityAInfo.name} vs {cityBInfo.name}
      </h1>
      <p className="text-gray-500 mb-8">
        Side-by-side salary comparison across {comparisons.length} common occupations
      </p>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <p className="text-sm text-gray-500 mb-1">{cityAInfo.name} Avg Median</p>
          <p className="text-2xl font-bold text-blue-600">
            {formatSalary(avgA, currencyA)}
          </p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <p className="text-sm text-gray-500 mb-1">Higher Pay Wins</p>
          <p className="text-lg font-bold">
            <span className="text-blue-600">{winsA}</span>
            <span className="text-gray-400 mx-2">-</span>
            <span className="text-purple-600">{winsB}</span>
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {winsA > winsB
              ? `${cityAInfo.name} pays more in ${winsA} of ${comparisons.length} roles`
              : winsB > winsA
              ? `${cityBInfo.name} pays more in ${winsB} of ${comparisons.length} roles`
              : "Tied across roles"}
          </p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4 text-center">
          <p className="text-sm text-gray-500 mb-1">{cityBInfo.name} Avg Median</p>
          <p className="text-2xl font-bold text-purple-600">
            {formatSalary(avgB, currencyB)}
          </p>
        </div>
      </div>

      {/* Comparison Table */}
      {comparisons.length > 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-xl font-bold mb-4">Salary Comparison by Role</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 font-medium text-gray-500">Occupation</th>
                  <th className="text-right py-3 font-medium text-blue-600">
                    {cityAInfo.name}
                  </th>
                  <th className="text-right py-3 font-medium text-purple-600">
                    {cityBInfo.name}
                  </th>
                  <th className="text-right py-3 font-medium text-gray-500">Difference</th>
                </tr>
              </thead>
              <tbody>
                {comparisons.map((c) => {
                  const diff = c.a.median_annual - c.b.median_annual;
                  const diffPct =
                    c.b.median_annual > 0
                      ? Math.round((diff / c.b.median_annual) * 100)
                      : 0;
                  return (
                    <tr key={c.occSlug} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3">
                        <Link
                          href={`/jobs/${c.occSlug}`}
                          className="text-blue-600 hover:underline"
                        >
                          {c.occName}
                        </Link>
                      </td>
                      <td className="text-right py-3 font-medium">
                        {formatSalary(c.a.median_annual, c.a.currency)}
                      </td>
                      <td className="text-right py-3 font-medium">
                        {formatSalary(c.b.median_annual, c.b.currency)}
                      </td>
                      <td
                        className={`text-right py-3 font-medium ${
                          diff > 0 ? "text-green-600" : diff < 0 ? "text-red-600" : "text-gray-400"
                        }`}
                      >
                        {diff > 0 ? "+" : ""}
                        {diffPct}%
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          {currencyA !== currencyB && (
            <p className="text-xs text-gray-400 mt-4">
              Note: {cityAInfo.name} salaries are in {currencyA} and {cityBInfo.name} salaries are in {currencyB}. Percentages reflect nominal differences.
            </p>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 p-6 text-center text-gray-500">
          No common occupations found between these cities.
        </div>
      )}

      {/* Cross-links */}
      <div className="mt-8 flex gap-4">
        <Link
          href={`/cities/${parsed.cityA}`}
          className="flex-1 bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow text-center"
        >
          <p className="font-semibold text-gray-900">All Jobs in {cityAInfo.name}</p>
          <p className="text-sm text-gray-500">{recordsA.length} occupations</p>
        </Link>
        <Link
          href={`/cities/${parsed.cityB}`}
          className="flex-1 bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow text-center"
        >
          <p className="font-semibold text-gray-900">All Jobs in {cityBInfo.name}</p>
          <p className="text-sm text-gray-500">{recordsB.length} occupations</p>
        </Link>
      </div>
    </div>
  );
}
