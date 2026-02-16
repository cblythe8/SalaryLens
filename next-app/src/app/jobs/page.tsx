import { Metadata } from "next";
import { getUniqueOccupations, getSalariesByOccupation } from "@/lib/data";
import JobsTable from "@/components/JobsTable";

export const metadata: Metadata = {
  title: "Browse Jobs - Salary Data by Occupation",
  description: "Explore salary data for 60+ occupations across the US. See median pay, salary ranges, and compare cities for every job title.",
};

export default function JobsPage() {
  const occupations = getUniqueOccupations();

  const occWithStats = occupations.map((occ) => {
    const records = getSalariesByOccupation(occ.slug);
    const medians = records.map((r) => r.median_annual).sort((a, b) => a - b);
    const avgMedian = Math.round(medians.reduce((a, b) => a + b, 0) / medians.length);
    return {
      ...occ,
      avgMedian,
      lowMedian: medians[0],
      highMedian: medians[medians.length - 1],
    };
  }).sort((a, b) => b.avgMedian - a.avgMedian);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Browse Jobs</h1>
      <p className="text-black mb-8">Salary data for {occupations.length} occupations</p>

      <JobsTable data={occWithStats} />
    </div>
  );
}
