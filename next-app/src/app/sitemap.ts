import { MetadataRoute } from "next";
import {
  getAllSlugs,
  getUniqueOccupations,
  getUniqueCities,
  getComparisonSlugs,
} from "@/lib/data";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://thesalarylens.com";

  const staticPages: MetadataRoute.Sitemap = [
    { url: baseUrl, lastModified: new Date(), changeFrequency: "weekly", priority: 1.0 },
    { url: `${baseUrl}/salaries`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/jobs`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/cities`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/compare`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.7 },
  ];

  const salaryPages: MetadataRoute.Sitemap = getAllSlugs().map((slug) => ({
    url: `${baseUrl}/salaries/${slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: 0.9,
  }));

  const jobPages: MetadataRoute.Sitemap = getUniqueOccupations().map((occ) => ({
    url: `${baseUrl}/jobs/${occ.slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: 0.8,
  }));

  const cityPages: MetadataRoute.Sitemap = getUniqueCities().map((city) => ({
    url: `${baseUrl}/cities/${city.slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: 0.8,
  }));

  const comparePages: MetadataRoute.Sitemap = getComparisonSlugs().map((slug) => ({
    url: `${baseUrl}/compare/${slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: 0.6,
  }));

  return [...staticPages, ...salaryPages, ...jobPages, ...cityPages, ...comparePages];
}
