# AIR2DNA architecture

AIR2DNA visualizes a curated mechanistic chain: exposure → cellular mechanism → DNA damage → repair → *potential* sequence/protein consequence. It does not calculate personal inhaled dose, mutation probability, cancer risk, or disease outcomes.

| Layer | Responsibility |
| --- | --- |
| `frontend/` | Next.js scenario inputs and scientific visualization. |
| `backend/` | FastAPI HTTP contract and input validation. |
| `science/` | Deterministic exposure descriptor, pathway graph, and Biopython annotation. |
| `data/` | Versionable verified evidence registry. |
| `tests/` | Calculation, pathway, and mutation classification coverage. |

Each pathway node owns an evidence level, an uncertainty statement, and references. Green means established mechanism; yellow means model-based/context dependent; grey means exploratory. Missing sources are never presented as verified.

`POST /trace` validates a scenario and returns a concentration-time descriptor plus a pathway graph. `POST /mutation` runs deterministic coding substitution annotation. A validated predictive ML model is deliberately absent: this MVP has no dataset sufficient to substantiate one.

`GET /air-quality/latest?region=central` is a server-side proxy for Singapore NEA's data.gov.sg PM2.5 API. It accepts only official reporting regions, reads `DATA_GOV_SG_API_KEY` from the server environment, applies a ten-second upstream timeout, and returns an upstream timestamp and a non-personal-exposure caveat. The frontend does not claim a stale/cache result is live and falls back to the fixed demo scenario on failure.
