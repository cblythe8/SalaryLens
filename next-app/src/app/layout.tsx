import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "SalaryLens - Salary Data for Every Job in Every City",
    template: "%s | SalaryLens",
  },
  description:
    "Explore salary data for thousands of jobs across US and Canadian metro areas. See median pay, salary ranges, and compare cities.",
  verification: {
    google: "AiWzsea52PHOXdciBBXv_A2p1zecscppJ5fPDeVYgvE",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased bg-gray-50 text-gray-900`}>
        <nav className="bg-white border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            <Link href="/" className="text-xl font-bold text-blue-600">
              SalaryLens
            </Link>
            <div className="flex gap-6 text-sm font-medium text-gray-600">
              <Link href="/salaries" className="hover:text-blue-600 transition-colors">
                Salaries
              </Link>
              <Link href="/jobs" className="hover:text-blue-600 transition-colors">
                Jobs
              </Link>
              <Link href="/cities" className="hover:text-blue-600 transition-colors">
                Cities
              </Link>
              <Link href="/compare" className="hover:text-blue-600 transition-colors">
                Compare
              </Link>
            </div>
          </div>
        </nav>
        <main>{children}</main>
        <footer className="bg-white border-t border-gray-200 mt-16">
          <div className="max-w-6xl mx-auto px-4 py-8 text-center text-sm text-gray-500">
            <p>Data sourced from the U.S. Bureau of Labor Statistics (BLS) and Statistics Canada.</p>
            <p className="mt-1">Salary figures are annual estimates and may vary based on experience, education, and other factors.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
