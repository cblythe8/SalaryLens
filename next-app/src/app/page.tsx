import Link from "next/link";
import SearchBar from "@/components/SearchBar";
import {
  getUniqueOccupations,
  getUniqueCities,
  getTopPayingRecords,
  formatSalary,
} from "@/lib/data";

export default function Home() {
  const occupations = getUniqueOccupations();
  const cities = getUniqueCities();
  const topPaying = getTopPayingRecords(6);

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div className="max-w-6xl mx-auto px-4 py-20 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            How Much Does Your Job Pay?
          </h1>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Real salary data for {occupations.length} occupations across{" "}
            {cities.length} cities in the US and Canada.
          </p>

          {/* Search */}
          <div className="max-w-xl mx-auto">
            <SearchBar />
          </div>

          <div className="flex flex-wrap justify-center gap-3 mt-8">
            <span className="text-blue-200 text-sm self-center">Popular:</span>
            {["software-developers", "registered-nurses", "data-scientists"].map(
              (slug) => {
                const occ = occupations.find((o) => o.slug === slug);
                if (!occ) return null;
                return (
                  <Link
                    key={slug}
                    href={`/jobs/${slug}`}
                    className="bg-white/10 hover:bg-white/20 px-4 py-2 rounded-full text-sm transition-colors"
                  >
                    {occ.name}
                  </Link>
                );
              }
            )}
          </div>
        </div>
      </section>

      {/* Top Paying */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold mb-6">Highest Paying Roles</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {topPaying.map((record) => {
            const citySlug = record.city_short.toLowerCase().replace(/\s+/g, "-");
            const slug = `${record.occ_slug}-in-${citySlug}`;
            return (
              <Link
                key={slug}
                href={`/salaries/${slug}`}
                className="bg-white rounded-lg border border-gray-200 p-5 hover:shadow-md transition-shadow"
              >
                <h3 className="font-semibold text-gray-900">{record.occ_name}</h3>
                <p className="text-sm text-gray-800 mb-3">
                  {record.city_short}, {record.state}
                </p>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-blue-600">
                    {formatSalary(record.median_annual, record.currency)}
                  </span>
                  <span className="text-sm text-gray-800">median</span>
                </div>
                <div className="mt-2 text-xs text-gray-800">
                  Range: {formatSalary(record.pct10_annual, record.currency)} &ndash;{" "}
                  {formatSalary(record.pct90_annual, record.currency)}
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Browse by Job */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold mb-6">Browse by Job Title</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {occupations.map((occ) => (
            <Link
              key={occ.slug}
              href={`/jobs/${occ.slug}`}
              className="bg-white rounded-lg border border-gray-200 px-4 py-3 text-sm text-gray-700 hover:text-blue-600 hover:border-blue-300 hover:shadow-sm transition-all"
            >
              {occ.name}
            </Link>
          ))}
        </div>
      </section>

      {/* Browse by City */}
      <section className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold mb-6">Browse by City</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {cities.map((city) => (
            <Link
              key={city.slug}
              href={`/cities/${city.slug}`}
              className="bg-white rounded-lg border border-gray-200 px-4 py-3 text-sm text-gray-700 hover:text-blue-600 hover:border-blue-300 hover:shadow-sm transition-all"
            >
              {city.name}, {city.state}
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
