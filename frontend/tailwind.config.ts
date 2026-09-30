import type { Config } from "tailwindcss";
export default { content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"], theme: { extend: { colors: { ink: "#07131e", panel: "#0b1c2a", cyan: "#65e5e0", lime: "#c5ef71", sun: "#f5bb64" } } }, plugins: [] } satisfies Config;
