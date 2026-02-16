"use client";

import { useState } from "react";
import Link from "next/link";
import { formatSalary } from "@/lib/data";

interface CityStats {
  slug: string;
  name: string;
  state: string;
  avgMedian: number;
  topJob: string;
  lowMedian: number;
  highMedian: number;
}

export default function CitiesTable({ data }: { data: CityStats[] }) {
  const [filter, setFilter] = useState("");
  const maxSalary = Math.max(...data.map((c) => c.avgMedian));

  const filtered = filter
    ? data.filter((city) =>
        `${city.name}, ${city.state}`.toLowerCase().includes(filter.toLowerCase())
      )
    : data;

  return (
    <>
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

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-sm text-black">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="text-left py-3 px-4 font-medium text-black">City</th>
              <th className="text-right py-3 px-4 font-medium text-black">Avg Median Salary</th>
              <th className="text-left py-3 px-4 font-medium text-black">Top Paying Job</th>
              <th className="text-right py-3 px-4 font-medium text-black">Salary Range</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((city) => (
              <tr key={city.slug} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <Link href={`/cities/${city.slug}`} className="text-blue-600 hover:underline font-medium">
                    {city.name}, {city.state}
                  </Link>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center justify-end gap-2">
                    <div className="hidden sm:block w-20 bg-gray-100 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full bg-blue-500 rounded-full"
                        style={{ width: `${(city.avgMedian / maxSalary) * 100}%` }}
                      />
                    </div>
                    <span className="font-medium whitespace-nowrap">{formatSalary(city.avgMedian)}</span>
                  </div>
                </td>
                <td className="py-3 px-4 text-black">
                  {city.topJob}
                </td>
                <td className="text-right py-3 px-4 text-black whitespace-nowrap">
                  {formatSalary(city.lowMedian)} - {formatSalary(city.highMedian)}
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={4} className="py-8 text-center text-black">
                  No cities match &ldquo;{filter}&rdquo;
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
