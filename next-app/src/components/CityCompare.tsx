"use client";

import { useState, useCallback } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface CityOption {
  slug: string;
  name: string;
  state: string;
}

interface ComparisonData {
  cities: { slug: string; name: string; state: string; currency: string }[];
  comparisons: {
    occSlug: string;
    occName: string;
    salaries: { median: number; currency: string }[];
  }[];
}

const COLORS = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b"];

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function CityCompare({ cities }: { cities: CityOption[] }) {
  const [selected, setSelected] = useState<string[]>(["", ""]);
  const [data, setData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(false);

  const canCompare = selected.filter(Boolean).length >= 2;
  const canAddMore = selected.length < 4;

  const handleCityChange = useCallback(
    (index: number, slug: string) => {
      const updated = [...selected];
      updated[index] = slug;
      setSelected(updated);
    },
    [selected]
  );

  const addCity = useCallback(() => {
    if (selected.length < 4) {
      setSelected([...selected, ""]);
    }
  }, [selected]);

  const removeCity = useCallback(
    (index: number) => {
      if (selected.length > 2) {
        setSelected(selected.filter((_, i) => i !== index));
      }
    },
    [selected]
  );

  const compare = useCallback(async () => {
    const slugs = selected.filter(Boolean);
    if (slugs.length < 2) return;

    setLoading(true);
    try {
      const res = await fetch(`/api/compare?cities=${slugs.join(",")}`);
      if (res.ok) {
        setData(await res.json());
      }
    } catch {
      // Request failed
    } finally {
      setLoading(false);
    }
  }, [selected]);

  // Build chart data (top 10 occupations)
  const chartData = data
    ? data.comparisons.slice(0, 10).map((c) => {
        const entry: Record<string, string | number> = { name: c.occName };
        data.cities.forEach((city, i) => {
          entry[`${city.name}, ${city.state}`] = c.salaries[i].median;
        });
        return entry;
      })
    : [];

  // Get used slugs (to prevent duplicates in dropdowns)
  const usedSlugs = new Set(selected.filter(Boolean));

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 mb-10">
      <h2 className="text-xl font-bold mb-4">Compare Cities</h2>
      <p className="text-black text-sm mb-4">
        Select 2-4 cities to compare salaries side by side.
      </p>

      {/* City selectors */}
      <div className="flex flex-wrap items-end gap-3 mb-4">
        {selected.map((slug, i) => (
          <div key={i} className="flex items-center gap-1">
            <select
              value={slug}
              onChange={(e) => handleCityChange(i, e.target.value)}
              className="px-3 py-2.5 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-black text-sm bg-white min-w-[180px]"
            >
              <option value="">Select a city...</option>
              {cities.map((city) => (
                <option
                  key={city.slug}
                  value={city.slug}
                  disabled={usedSlugs.has(city.slug) && slug !== city.slug}
                >
                  {city.name}, {city.state}
                </option>
              ))}
            </select>
            {selected.length > 2 && (
              <button
                onClick={() => removeCity(i)}
                className="text-black hover:text-red-600 p-1 text-sm"
                aria-label="Remove city"
              >
                &#10005;
              </button>
            )}
          </div>
        ))}

        {canAddMore && (
          <button
            onClick={addCity}
            className="text-sm text-blue-600 hover:underline px-2 py-2.5"
          >
            + Add City
          </button>
        )}

        <button
          onClick={compare}
          disabled={!canCompare || loading}
          className="bg-blue-600 text-white text-sm font-medium px-5 py-2.5 rounded-lg hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Loading..." : "Compare"}
        </button>
      </div>

      {/* Results */}
      {data && (
        <>
          {/* Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            {data.cities.map((city, i) => {
              const avgMedian =
                data.comparisons.length > 0
                  ? Math.round(
                      data.comparisons.reduce((s, c) => s + c.salaries[i].median, 0) /
                        data.comparisons.length
                    )
                  : 0;
              return (
                <div
                  key={city.slug}
                  className="rounded-lg border p-3 text-center"
                  style={{ borderColor: COLORS[i] }}
                >
                  <p className="text-sm font-medium text-black">
                    {city.name}, {city.state}
                  </p>
                  <p className="text-lg font-bold" style={{ color: COLORS[i] }}>
                    {formatCurrency(avgMedian)}
                  </p>
                  <p className="text-xs text-black">Avg Median ({city.currency})</p>
                </div>
              );
            })}
          </div>

          {/* Bar chart */}
          {chartData.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-black mb-3">
                Top 10 Highest Paying Jobs (Median Salary)
              </h3>
              <div className="w-full" style={{ height: 420 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={chartData}
                    layout="vertical"
                    margin={{ top: 0, right: 20, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis
                      type="number"
                      tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                      tick={{ fill: "#000", fontSize: 12 }}
                    />
                    <YAxis
                      dataKey="name"
                      type="category"
                      width={160}
                      tick={{ fill: "#000", fontSize: 11 }}
                    />
                    <Tooltip
                      formatter={(value) => formatCurrency(Number(value))}
                      contentStyle={{ fontSize: 13 }}
                    />
                    <Legend />
                    {data.cities.map((city, i) => (
                      <Bar
                        key={city.slug}
                        dataKey={`${city.name}, ${city.state}`}
                        fill={COLORS[i]}
                        radius={[0, 4, 4, 0]}
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Comparison table */}
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-black">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 font-medium text-black">Occupation</th>
                  {data.cities.map((city, i) => (
                    <th
                      key={city.slug}
                      className="text-right py-3 font-medium"
                      style={{ color: COLORS[i] }}
                    >
                      {city.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.comparisons.map((c) => (
                  <tr key={c.occSlug} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-2.5 text-black">{c.occName}</td>
                    {c.salaries.map((s, i) => (
                      <td key={i} className="text-right py-2.5 font-medium">
                        {formatCurrency(s.median)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <p className="text-xs text-black mt-3">
            Showing {data.comparisons.length} occupations common across all selected cities.
            {data.cities.some((c) => c.currency !== data.cities[0].currency) &&
              " Note: Cities may use different currencies (USD/CAD). Values shown are nominal."}
          </p>
        </>
      )}
    </div>
  );
}
