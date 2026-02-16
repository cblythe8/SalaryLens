"use client";

import { useState } from "react";
import Link from "next/link";
import { formatSalary } from "@/lib/data";

interface OccStats {
  slug: string;
  name: string;
  avgMedian: number;
  lowMedian: number;
  highMedian: number;
}

export default function JobsTable({ data }: { data: OccStats[] }) {
  const [filter, setFilter] = useState("");

  const filtered = filter
    ? data.filter((occ) =>
        occ.name.toLowerCase().includes(filter.toLowerCase())
      )
    : data;

  return (
    <>
      <div className="mb-4">
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter jobs..."
          className="w-full max-w-sm px-4 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-black text-sm"
        />
        {filter && (
          <p className="text-xs text-black mt-2">
            Showing {filtered.length} of {data.length} jobs
          </p>
        )}
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-sm text-black">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left py-3 px-4 font-medium text-black">Job Title</th>
              <th className="text-right py-3 px-4 font-medium text-black">Avg Median Salary</th>
              <th className="text-right py-3 px-4 font-medium text-black">Salary Range</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((occ) => (
              <tr key={occ.slug} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <Link href={`/jobs/${occ.slug}`} className="text-blue-600 hover:underline font-medium">
                    {occ.name}
                  </Link>
                </td>
                <td className="text-right py-3 px-4 font-medium">
                  {formatSalary(occ.avgMedian)}
                </td>
                <td className="text-right py-3 px-4 text-black whitespace-nowrap">
                  {formatSalary(occ.lowMedian)} - {formatSalary(occ.highMedian)}
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={3} className="py-8 text-center text-black">
                  No jobs match &ldquo;{filter}&rdquo;
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
