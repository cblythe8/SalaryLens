import { Metadata } from "next";
import { getUniqueCities, getSalariesByCity, getCityContent } from "@/lib/data";
import CitiesTable from "@/components/CitiesTable";

export const metadata: Metadata = {
  title: "Browse Cities - Salary Data by Location",
  description: "Compare salaries across 50+ US metro areas. Find the highest paying cities for your occupation.",
};

export default function CitiesPage() {
  const cities = getUniqueCities();

  const cityWithStats = cities.map((city) => {
    const records = getSalariesByCity(city.slug);
    const medians = records.map((r) => r.median_annual).sort((a, b) => a - b);
    const avgMedian = Math.round(medians.reduce((a, b) => a + b, 0) / medians.length);
    const content = getCityContent(city.slug);
    return {
      ...city,
      avgMedian,
      costOfLiving: content?.cost_of_living || null,
      lowMedian: medians[0],
      highMedian: medians[medians.length - 1],
    };
  }).sort((a, b) => b.avgMedian - a.avgMedian);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Browse Cities</h1>
      <p className="text-black mb-8">Salary data across {cities.length} US metro areas</p>

      <CitiesTable data={cityWithStats} />
    </div>
  );
}
