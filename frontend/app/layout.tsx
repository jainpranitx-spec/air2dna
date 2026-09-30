import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "AIR2DNA | Trace the Path", description: "An evidence-bounded environmental molecular biology explorer." };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en"><body>{children}</body></html>; }
