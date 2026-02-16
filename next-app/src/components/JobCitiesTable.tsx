"use client";

import { useState } from "react";
import Link from "next/link";
import { formatSalary } from "@/lib/data";

interface SalaryRecord {
  area_code: string;
  occ_slug: string;
  occ_name: string;
  city_short: string;
  state: string;
  currency: string;
  median_annual: number;
  mean_annual: number;
  pct10_annual: number;
  pct90_annual: number;
}

export default function JobCitiesTable({
  data,
  jobName,
}: {
  data: SalaryRecord[];
  jobName: string;
}) {
  const [filter, setFilter] = useState("");

  const maxMedian = Math.max(...data.map((r) => r.median_annual));

  const filtered = filter
    ? data.filter((r) =>
        `${r.city_short}, ${r.state}`.toLowerCase().includes(filter.toLowerCase())
      )
    : data;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-xl font-bold mb-4">{jobName} Salary by City</h2>

      <div className="mb-4">
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter cities..."
          className="w-full max-w-sm px-4 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-black text-sm"
        />
        {filter && (
          <p className="text-xs text-black mt-2">
            Showing {filtered.length} of {data.length} cities
          </p>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm text-black">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 font-medium text-black">City</th>
              <th className="text-right py-3 font-medium text-black">Median</th>
              <th className="text-right py-3 font-medium text-black">Average</th>
              <th className="text-right py-3 font-medium text-black">Range (10th-90th)</th>
              <th className="text-center py-3 font-medium text-black">Currency</th>
              <th className="text-right py-3 font-medium text-black"></th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((r) => {
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
                  <td className="py-3">
                    <div className="flex items-center justify-end gap-2">
                      <div className="hidden sm:block w-16 bg-gray-100 rounded-full h-2 overflow-hidden">
                        <div
                          className="h-full bg-blue-500 rounded-full"
                          style={{ width: `${(r.median_annual / maxMedian) * 100}%` }}
                        />
                      </div>
                      <span className="font-medium whitespace-nowrap">{formatSalary(r.median_annual, r.currency)}</span>
                    </div>
                  </td>
                  <td className="text-right py-3 text-black">
                    {formatSalary(r.mean_annual, r.currency)}
                  </td>
                  <td className="text-right py-3 text-black">
                    {formatSalary(r.pct10_annual, r.currency)} - {formatSalary(r.pct90_annual, r.currency)}
                  </td>
                  <td className="text-center py-3">
                    <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${r.currency === "CAD" ? "bg-red-50 text-red-700" : "bg-blue-50 text-blue-700"}`}>
                      {r.currency}
                    </span>
                  </td>
                  <td className="text-right py-3">
                    <a
                      href={`https://www.indeed.com/jobs?q=${encodeURIComponent(jobName)}&l=${encodeURIComponent(r.city_short + ", " + r.state)}`}
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
            {filtered.length === 0 && (
              <tr>
                <td colSpan={6} className="py-8 text-center text-black">
                  No cities match &ldquo;{filter}&rdquo;
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
