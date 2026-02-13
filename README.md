# SalaryLens

A programmatic SEO salary comparison website that auto-generates 31,000+ pages targeting long-tail search queries like *"Software Developer salary in San Francisco"* or *"Nurse salary in Toronto."*

## Key Numbers

- **489** occupations (from Anesthesiologist to Barista)
- **60** cities (50 US metros + 10 Canadian cities)
- **29,340** salary records
- **31,659** auto-generated pages

## How It Works

1. A **Python data pipeline** generates salary data based on published BLS (Bureau of Labor Statistics) national medians, adjusted for each metro area's cost of living
2. **Next.js** turns every job-city combination into a unique, SEO-optimized page with structured data (JSON-LD), internal linking, and meta tags
3. An auto-generated **sitemap.xml** with 31k+ URLs helps Google discover and index every page

## Page Types

| Type | Example URL | Description |
|------|-------------|-------------|
| Salary | `/salaries/software-developers-in-new-york` | Median, mean, percentile ranges (10th–90th), employment data |
| Job | `/jobs/software-developers` | One job's salary across all 60 cities |
| City | `/cities/san-francisco` | All salaries in a city, ranked highest to lowest |
| Compare | `/compare/new-york-vs-san-francisco` | Side-by-side salary tables for two cities |

## Tech Stack

- **Frontend:** Next.js 16 (App Router), TypeScript, Tailwind CSS
- **Data Pipeline:** Python
- **Search:** Server-side API route with debounced client requests
- **SEO:** JSON-LD structured data, auto-generated sitemap, internal linking
- **Hosting:** Vercel

## Getting Started

```bash
# Install dependencies
cd next-app && npm install

# Run the dev server
npm run dev
# Open http://localhost:3000
```

### Regenerate Salary Data

```bash
cd data
python3 generate_full_data.py
```

### Optional: Pull Real BLS Data

Get a free API key at [data.bls.gov/registrationEngine](https://data.bls.gov/registrationEngine/), then:

```bash
BLS_API_KEY=your_key python3 data/build_from_api.py
```

## Project Structure

```
salary-site/
├── data/                           # Python data pipeline
│   ├── generate_full_data.py       # Main generator (489 jobs × 60 cities)
│   └── build_from_api.py           # Optional real BLS data fetcher
├── next-app/                       # Next.js frontend
│   └── src/
│       ├── app/                    # Pages (salary, job, city, compare)
│       ├── components/             # SearchBar
│       └── lib/                    # Data utilities + salary_data.json
└── README.md
```
