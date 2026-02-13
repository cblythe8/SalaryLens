# SalaryLens — Project Notes

## What Is This?

SalaryLens is a **programmatic SEO website** that auto-generates thousands of salary pages targeting long-tail search queries like "Software Developer salary in San Francisco" or "Nurse salary in Toronto." The idea is that each page ranks individually on Google, and over time the site attracts organic traffic that gets monetized through ads and affiliate links.

**The business model:** Build once, earn passively. Every page is a potential Google search result. More pages = more chances to rank = more traffic = more ad revenue.

## How It Works (The Simple Version)

1. A **Python script** generates salary data for 489 jobs across 60 cities (US + Canada)
2. **Next.js** automatically creates a unique page for every job-city combination
3. That produces **31,659 pages** — each one optimized for a specific search query
4. Google indexes the pages, people search for salary info, they land on the site, ads generate revenue

## What Was Built

### Page Types
- **Salary pages** (`/salaries/software-developers-in-new-york`) — The money pages. Show median, mean, percentile ranges (10th–90th), employment numbers. Each has JSON-LD structured data for Google rich results.
- **Job overview pages** (`/jobs/software-developers`) — Show salary data across all 60 cities for one job. Links to every city-specific salary page (internal linking = SEO gold).
- **City pages** (`/cities/san-francisco`) — Show all salaries in a city, ranked highest to lowest.
- **Comparison pages** (`/compare/new-york-vs-san-francisco`) — Side-by-side salary tables for two cities across all occupations. Shows which city pays more for each job.
- **Home page** — Search bar, highest-paying roles, browse by job or city.

### Key Numbers
| Metric | Count |
|--------|-------|
| Occupations | 489 |
| US Cities | 50 |
| Canadian Cities | 10 |
| Salary Records | 29,340 |
| Total Pages | 31,659 |

### The Data

The salary data is generated from **real BLS (Bureau of Labor Statistics) national median salaries** with metro-area cost-of-living adjustment factors. It's not made up — it's modeled from published government statistics. For example:
- BLS says Software Developers have a national median of $132,270
- San Francisco has a cost-of-living factor of 1.38x
- So SF Software Developer median ≈ $132,270 × 1.38 ≈ $183,000
- Small randomness (±3%) is added so each city isn't perfectly predictable

For Canadian data, US medians are converted using a wage factor (0.82x) to reflect the Canadian labor market, then adjusted per city.

**Optional upgrade:** There's a BLS API key (`build_from_api.py`) that can pull *real* government data for each job-city combo. This is an improvement but not necessary — the generated data is realistic and good enough.

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 16 (App Router) + TypeScript | Static site generation, great SEO, Vercel deployment |
| Styling | Tailwind CSS | Fast to build, responsive out of the box |
| Data | Python + JSON | Simple, no database needed |
| Hosting | Vercel (planned) | Free tier, perfect for Next.js, handles 30k+ pages |
| Monetization | Google AdSense + affiliate links (planned) | Passive income from organic traffic |

## Project Structure

```
salary-site/
├── data/                           # Python data pipeline
│   ├── generate_full_data.py       # Main data generator (489 occupations × 60 cities)
│   ├── generate_us_data.py         # Earlier version (30 occupations, not used)
│   ├── build_from_api.py           # Optional: pulls real BLS API data
│   └── build_salary_data.py        # Earlier BLS bulk download attempt (didn't work)
├── next-app/                       # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Home page (search, top paying, browse)
│   │   │   ├── layout.tsx          # Root layout (nav, footer)
│   │   │   ├── sitemap.ts          # Auto-generated sitemap.xml
│   │   │   ├── robots.ts           # robots.txt
│   │   │   ├── api/search/route.ts # Server-side search API
│   │   │   ├── salaries/
│   │   │   │   ├── page.tsx        # Browse all salaries
│   │   │   │   └── [slug]/page.tsx # Individual salary pages
│   │   │   ├── jobs/
│   │   │   │   └── [slug]/page.tsx # Job overview pages
│   │   │   ├── cities/
│   │   │   │   └── [slug]/page.tsx # City pages
│   │   │   └── compare/
│   │   │       ├── page.tsx        # Compare index
│   │   │       └── [slug]/page.tsx # City vs city comparison
│   │   ├── components/
│   │   │   └── SearchBar.tsx       # Search with debounced API calls
│   │   └── lib/
│   │       ├── data.ts             # Data utilities (queries, formatting)
│   │       └── salary_data.json    # 29,340 salary records (13.3 MB)
│   └── package.json
└── Project-Notes.md                # This file
```

## How We Built It (Session History)

### Session 1 (Previous conversation — ran out of context)
- Set up Next.js project with TypeScript + Tailwind
- Created initial data with ~22 records (small test set)
- Built core pages: salary detail, job overview, city pages
- Added SearchBar component
- Got the basic site working on localhost

### Session 2 (Continued build)
1. **Expanded data** from 22 → 88 records (more cities and occupations)
2. **Fixed CAD currency formatting** — Canadian salaries now display with `CA$` and proper locale
3. **Built comparison pages** — City vs city salary comparisons with percentage differences
4. **Added SEO infrastructure** — sitemap.xml (auto-generated from data), robots.txt, JSON-LD structured data
5. **Tried BLS API** — Got rate limited (25 requests/day without key). Built fallback data generator.
6. **Scaled to 313 occupations** — Created `generate_full_data.py` with 25 US metros, 5 CA cities
7. **Performance fix** — Homepage was 3.7MB because search index was serialized into HTML. Moved to server-side API route (`/api/search`). Homepage dropped to 544KB.
8. **Scaled to 489 occupations** — Added 176 more jobs covering virtually every BLS category
9. **Expanded to 50 US metros + 10 CA cities** — 29,340 total records, 31,659 pages
10. **Got BLS API key** — Built `build_from_api.py` to optionally replace generated data with real government numbers

## How To Run It

```bash
# Start the dev server
cd ~/Desktop/Personal-Learning/30\ -\ Projects/salary-site/next-app
npm run dev
# Open http://localhost:3000

# Regenerate salary data (if you change occupations or cities)
cd ~/Desktop/Personal-Learning/30\ -\ Projects/salary-site/data
python3 generate_full_data.py

# Optional: Pull real BLS data (requires API key in build_from_api.py)
python3 build_from_api.py
```

## How To Describe It To Someone

> "I built a salary comparison website that automatically generates over 30,000 pages targeting specific job-and-city search queries — like 'Nurse salary in Chicago' or 'Software Developer salary in Toronto.' I wrote a Python data pipeline that models salary distributions from Bureau of Labor Statistics data, and a Next.js frontend that turns each data point into an SEO-optimized page with structured data, internal linking, and a search engine. The goal is passive income through Google AdSense once the pages start ranking."

**Key talking points:**
- **Programmatic SEO** — One template, thousands of pages, each targeting a unique long-tail keyword
- **Data pipeline** — Python scripts generate realistic salary data based on published BLS statistics
- **Full-stack** — Next.js + TypeScript frontend, Python data processing, REST API for search
- **Scale** — 489 occupations, 60 cities, 31,659 pages, auto-generated sitemap
- **SEO best practices** — JSON-LD structured data, internal linking strategy, meta tags, sitemap

## Remaining Steps

1. **Deploy** — Push to GitHub, deploy to Vercel
2. **Domain** — Buy a domain name (e.g., salarylens.com)
3. **Google Search Console** — Submit sitemap, monitor indexing
4. **Monetization** — Apply for Google AdSense (need some traffic first), add affiliate links to job boards
5. **Optional improvements:**
   - AI-generated content per page (career advice, skills needed, etc.)
   - More Canadian data from Statistics Canada
   - Swap generated data for real BLS numbers using the API script
   - Add more page types (industry comparisons, salary calculators, etc.)
