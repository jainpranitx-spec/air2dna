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

// Vercel Services injects NEXT_PUBLIC_BACKEND_URL as the deployment-aware public
// route prefix. Local standalone development can use NEXT_PUBLIC_API_URL instead.
const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "/api";

export async function fetchLatestPM25(region = "central"): Promise<LivePM25> {
  const response = await fetch(`${API_URL}/air-quality/latest?region=${encodeURIComponent(region)}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    const rawBody = await response.text();
    try {
      const body = JSON.parse(rawBody) as { detail?: string };
      throw new Error(body.detail ?? `AIR2DNA API returned HTTP ${response.status}.`);
    } catch (error) {
      if (error instanceof SyntaxError) {
        throw new Error(`AIR2DNA API returned HTTP ${response.status}, not a JSON response. Check /api/health and the backend Function logs.`);
      }
      throw error;
    }
  }
  try {
    return JSON.parse(await response.text()) as LivePM25;
  } catch {
    throw new Error("AIR2DNA API returned an invalid live-data response. Check the backend Function logs.");
  }
}