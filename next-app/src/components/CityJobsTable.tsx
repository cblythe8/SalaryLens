"use client";

import { useState } from "react";
import Link from "next/link";
import { formatSalary, formatNumber } from "@/lib/data";

interface SalaryRecord {
  area_code: string;
  occ_code: string;
  occ_name: string;
  occ_slug: string;
  city_short: string;
  state: string;
  currency: string;
  median_annual: number;
  pct10_annual: number;
  pct90_annual: number;
  employment: number;
}

export default function CityJobsTable({
  data,
  cityName,
}: {
  data: SalaryRecord[];
  cityName: string;
}) {
  const [filter, setFilter] = useState("");
  const [minSalary, setMinSalary] = useState("");
  const [maxSalary, setMaxSalary] = useState("");

  const min = minSalary ? parseInt(minSalary, 10) : 0;
  const max = maxSalary ? parseInt(maxSalary, 10) : Infinity;

  const filtered = data.filter((r) => {
    const matchesText = filter
      ? r.occ_name.toLowerCase().includes(filter.toLowerCase())
      : true;
    const matchesRange = r.median_annual >= min && r.median_annual <= max;
    return matchesText && matchesRange;
  });

  const hasFilters = filter || minSalary || maxSalary;
  const maxMedian = Math.max(...data.map((r) => r.median_annual));

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h2 className="text-xl font-bold mb-4">All Salaries in {cityName}</h2>

      {/* Filters */}
      <div className="flex flex-wrap items-end gap-3 mb-4">
        <div>
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Filter by job title..."
            className="px-4 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-black text-sm w-56"
          />
        </div>
        <div className="flex items-center gap-2">
          <input
            type="number"
            value={minSalary}
            onChange={(e) => setMinSalary(e.target.value)}
            placeholder="Min salary"
            className="px-3 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-black text-sm w-32"
          />
          <span className="text-black text-sm">to</span>
          <input
            type="number"
            value={maxSalary}
            onChange={(e) => setMaxSalary(e.target.value)}
            placeholder="Max salary"
            className="px-3 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-black text-sm w-32"
          />
        </div>
        {hasFilters && (
          <button
            onClick={() => {
              setFilter("");
              setMinSalary("");
              setMaxSalary("");
            }}
            className="text-sm text-blue-600 hover:underline"
          >
            Clear filters
          </button>
        )}
      </div>

      {hasFilters && (
        <p className="text-xs text-black mb-3">
          Showing {filtered.length} of {data.length} jobs
        </p>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-black">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 pr-4 font-medium text-black">Job Title</th>
              <th className="text-right py-3 px-3 font-medium text-black">Median</th>
              <th className="text-right py-3 px-3 font-medium text-black">Range (10th-90th)</th>
              <th className="text-right py-3 px-3 font-medium text-black">Est. Employed*</th>
              <th className="text-right py-3 pl-3 font-medium text-black"></th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((r) => {
              const citySlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
              return (
                <tr key={r.occ_code} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 pr-4">
                    <Link
                      href={`/salaries/${r.occ_slug}-in-${citySlug}`}
                      className="text-blue-600 hover:underline"
                    >
                      {r.occ_name}
                    </Link>
                  </td>
                  <td className="py-3 px-3">
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
                  <td className="text-right py-3 px-3 text-black whitespace-nowrap">
                    {formatSalary(r.pct10_annual, r.currency)} - {formatSalary(r.pct90_annual, r.currency)}
                  </td>
                  <td className="text-right py-3 px-3 text-black whitespace-nowrap">
                    {formatNumber(r.employment)}
                  </td>
                  <td className="text-right py-3 pl-3">
                    <a
                      href={`https://www.indeed.com/jobs?q=${encodeURIComponent(r.occ_name)}&l=${encodeURIComponent(r.city_short + ", " + r.state)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline text-xs whitespace-nowrap"
                    >
                      Apply
                    </a>
                  </td>
                </tr>
              );
            })}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={5} className="py-8 text-center text-black">
                  No jobs match your filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-black mt-4">
        *Employment figures are estimates based on national occupational data distributed across metro areas. Actual local numbers may vary.
      </p>
    </div>
  );
}
