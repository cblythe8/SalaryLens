import salaryData from "./salary_data.json";
import occupationContentData from "./occupation_content.json";
import cityContentData from "./city_content.json";

export interface SalaryRecord {
  area_code: string;
  area_name: string;
  city_short: string;
  state: string;
  country: string;
  currency: string;
  occ_code: string;
  occ_name: string;
  occ_slug: string;
  employment: number;
  mean_annual: number;
  median_annual: number;
  pct10_annual: number;
  pct25_annual: number;
  pct75_annual: number;
  pct90_annual: number;
}

export interface OccupationContent {
  soc_group: string;
  description: string;
  skills: string[];
  education: string;
  education_detail: string;
  career_outlook: string;
  salary_tips: string[];
  work_environment: string;
  related_occupations: string[];
}

export interface CityContent {
  overview: string;
  top_industries: string[];
  cost_of_living: string;
  cost_of_living_detail: string;
}

const data: SalaryRecord[] = salaryData as SalaryRecord[];
const occContent: Record<string, OccupationContent> = occupationContentData as Record<string, OccupationContent>;
const ctyContent: Record<string, CityContent> = cityContentData as Record<string, CityContent>;

export function getAllSalaryRecords(): SalaryRecord[] {
  return data;
}

export function getSalaryBySlug(slug: string): SalaryRecord | undefined {
  // slug format: "software-developers-in-new-york"
  return data.find((r) => {
    const citySlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
    return `${r.occ_slug}-in-${citySlug}` === slug;
  });
}

export function getSalaryByOccupationAndCity(
  occSlug: string,
  citySlug: string
): SalaryRecord | undefined {
  return data.find((r) => {
    const cSlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
    return r.occ_slug === occSlug && cSlug === citySlug;
  });
}

export function getAllSlugs(): string[] {
  return data.map((r) => {
    const citySlug = r.city_short.toLowerCase().replace(/\s+/g, "-");
    return `${r.occ_slug}-in-${citySlug}`;
  });
}

export function getUniqueOccupations(): { slug: string; name: string }[] {
  const seen = new Set<string>();
  const result: { slug: string; name: string }[] = [];
  for (const r of data) {
    if (!seen.has(r.occ_slug)) {
      seen.add(r.occ_slug);
      result.push({ slug: r.occ_slug, name: r.occ_name });
    }
  }
  return result.sort((a, b) => a.name.localeCompare(b.name));
}

export function getUniqueCities(): { slug: string; name: string; state: string }[] {
  const seen = new Set<string>();
  const result: { slug: string; name: string; state: string }[] = [];
  for (const r of data) {
    const slug = r.city_short.toLowerCase().replace(/\s+/g, "-");
    if (!seen.has(slug)) {
      seen.add(slug);
      result.push({ slug, name: r.city_short, state: r.state });
    }
  }
  return result.sort((a, b) => a.name.localeCompare(b.name));
}

export function getSalariesByOccupation(occSlug: string): SalaryRecord[] {
  return data.filter((r) => r.occ_slug === occSlug);
}

export function getSalariesByCity(citySlug: string): SalaryRecord[] {
  return data.filter((r) => {
    const slug = r.city_short.toLowerCase().replace(/\s+/g, "-");
    return slug === citySlug;
  });
}

export function getTopPayingRecords(limit: number = 6): SalaryRecord[] {
  return [...data]
    .sort((a, b) => b.median_annual - a.median_annual)
    .slice(0, limit);
}

export function formatSalary(amount: number, currency: string = "USD"): string {
  const locale = currency === "CAD" ? "en-CA" : "en-US";
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat("en-US").format(num);
}

export function getComparisonSlugs(): string[] {
  const cities = getUniqueCities();
  const slugs: string[] = [];
  for (let i = 0; i < cities.length; i++) {
    for (let j = i + 1; j < cities.length; j++) {
      slugs.push(`${cities[i].slug}-vs-${cities[j].slug}`);
    }
  }
  return slugs;
}

export function getOccupationContent(occSlug: string): OccupationContent | undefined {
  return occContent[occSlug];
}

export function getCityContent(citySlug: string): CityContent | undefined {
  return ctyContent[citySlug];
}

export function parseComparisonSlug(slug: string): { cityA: string; cityB: string } | null {
  const cities = getUniqueCities();
  const citySlugs = cities.map((c) => c.slug);

  for (const citySlug of citySlugs) {
    if (slug.startsWith(citySlug + "-vs-")) {
      const rest = slug.slice(citySlug.length + 4);
      if (citySlugs.includes(rest)) {
        return { cityA: citySlug, cityB: rest };
      }
    }
  }
  return null;
}
