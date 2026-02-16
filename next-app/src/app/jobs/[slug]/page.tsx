import { notFound } from "next/navigation";
import Link from "next/link";
import { Metadata } from "next";
import {
  getUniqueOccupations,
  getSalariesByOccupation,
  getOccupationContent,
  formatSalary,
} from "@/lib/data";
import JobCitiesTable from "@/components/JobCitiesTable";

export const dynamic = "force-dynamic";

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

  const content = getOccupationContent(slug);

  const avgMedian = Math.round(
    records.reduce((sum, r) => sum + r.median_annual, 0) / records.length
  );

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <nav className="text-sm text-black mb-6">
        <Link href="/" className="hover:text-blue-600">Home</Link>
        {" / "}
        <Link href="/jobs" className="hover:text-blue-600">Jobs</Link>
        {" / "}
        <span className="text-black">{name}</span>
      </nav>

      <h1 className="text-3xl md:text-4xl font-bold mb-2">
        {name} Salary
      </h1>
      <p className="text-black mb-8">
        Salary data across {records.length} metro areas in the US &amp; Canada
        <span className="ml-2 text-xs px-2 py-0.5 rounded font-medium bg-gray-100 text-gray-700">
          USD &amp; CAD
        </span>
      </p>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-black">Avg Median Salary</p>
          <p className="text-2xl font-bold text-blue-600">{formatSalary(avgMedian)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-black">Highest Paying City</p>
          <p className="text-lg font-bold">{sorted[0].city_short}</p>
          <p className="text-sm text-black">{formatSalary(sorted[0].median_annual)}</p>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-black">Cities Tracked</p>
          <p className="text-2xl font-bold">{records.length}</p>
        </div>
      </div>

      {/* Career Overview */}
      {content && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-3">What Do {name} Do?</h2>
          <p className="text-black leading-relaxed">{content.description}</p>
          {content.work_environment && (
            <p className="text-black mt-3 text-sm">{content.work_environment}</p>
          )}
        </div>
      )}

      {/* Key Skills */}
      {content?.skills && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-4">Key Skills for {name}</h2>
          <div className="flex flex-wrap gap-2">
            {content.skills.map((skill) => (
              <span key={skill} className="bg-blue-50 text-blue-700 px-3 py-1.5 rounded-full text-sm font-medium">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Education + Career Outlook */}
      {content && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-bold mb-2">Education Requirements</h2>
            <p className="text-sm font-medium text-blue-600 mb-2">{content.education}</p>
            <p className="text-black text-sm">{content.education_detail}</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-bold mb-2">Career Outlook</h2>
            <p className="text-black text-sm">{content.career_outlook}</p>
          </div>
        </div>
      )}

      {/* Salary Tips */}
      {content?.salary_tips && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
          <h2 className="text-xl font-bold mb-4">How to Increase Your {name} Salary</h2>
          <ul className="space-y-3">
            {content.salary_tips.map((tip, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="text-blue-500 font-bold mt-0.5">{i + 1}.</span>
                <span className="text-black">{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* All Cities Table */}
      <JobCitiesTable data={sorted} jobName={name} />
    </div>
  );
}
