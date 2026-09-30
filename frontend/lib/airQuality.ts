export type LivePM25 = {
  source: string;
  timestamp: string;
  updated_at: string;
  region: string;
  pm25_ug_m3: number | null;
  national_pm25_ug_m3: number | null;
  unit: "µg/m³";
  freshness_note: string;
};

// Production uses the same-domain Vercel rewrite. Local standalone development
// can set NEXT_PUBLIC_API_URL=http://localhost:8000 in frontend/.env.local.
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "/api";

export async function fetchLatestPM25(region = "central"): Promise<LivePM25> {
  const response = await fetch(`${API_URL}/air-quality/latest?region=${encodeURIComponent(region)}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    const body: { detail?: string } = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "Unable to load the latest NEA PM2.5 reading.");
  }
  return response.json() as Promise<LivePM25>;
}
