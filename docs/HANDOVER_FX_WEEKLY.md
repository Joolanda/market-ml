# Handover – FX Weekly (branch `feature/fx-weekly`)

Context for continuing this work in a new Claude project / session.

## Goal
Turn the bootcamp project (next-candle prediction for BTC) into a portfolio piece for
consultancy / banking engineering interviews (e.g. Sparkasse, Raiffeisen):
**a data-driven "FX Weekly"**, inspired by ABN AMRO's FX Weekly (Georgette Boele).

Story: *"A multi-market ML pipeline (EUR/USD, EUR/CHF, EUR/PLN + BTC) that shows weekly
risk and outlook, honestly validated against a random walk, explainable, and deployed as a
container on AWS."*

## Decisions taken
- Markets: EUR/USD, EUR/CHF, EUR/PLN (CEE, relevant for Raiffeisen) + BTC/USD (kept: Sparkassen
  started crypto trading in their app on 19 Oct 2026; RBI rolls out crypto via Bitpanda).
- Horizon: weekly (Friday close). Outputs: P(up next week), 80% expected range, volatility regime.
- Benchmarks: random walk (Theil's U), training up-share (direction), 4-week average vol.
- Data: Yahoo Finance daily OHLCV + FRED/OECD 3-month interbank rates (no API keys).
  Seeded **sample data** is used automatically when `data/raw/` is empty (offline / CI).
- AWS: one container (ECS Express Mode or Lightsail Containers). Not EKS. App Runner takes
  no new customers since 30 Apr 2026.

## Done in this branch
Data and models (session 1):
- `.gitignore`: only top-level `/data/` ignored (before, `data/` also hid `src/data/` and
  `streamlit_app/data/`, which is why the app did not start from a fresh clone).
- `src/config/assets.py` – asset registry + FRED rate series.
- `src/data/` – sources (Yahoo / FRED), seeded sample data, single data loader.
- `streamlit_app/data/` – live price + feature loaders with offline fallback; `ta_logic.py` pandas import.
- `src/fx/weekly.py` – weekly features/targets incl. rate differential (with publication lag).
- `src/fx/models.py` – logistic / ridge / HAR-vol models + walk-forward + evaluation.

Report, app, tests, CI (session 2, 11 Nov 2026):
- `src/fx/report.py` – `AssetOutlook` per market, Markdown report + track record;
  CLI `fetch-data [--strict]`, `fx-weekly`, `fx-eval`. Sample report in `reports/fx_weekly/`.
- Streamlit page `streamlit_app/pages/fx_weekly.py` (default page): metrics, chart with
  out-of-sample 80% band + next week's range, drivers, track record, method.
  Debug output removed from `overview.py`; `predictions.py` shows a note without the 15m CSV;
  sidebar text contrast fixed.
- `tests/test_fx_weekly.py` – 19 tests (look-ahead, rate publication lag, walk-forward only
  on past weeks, report for all assets, page imports, page renders). Run on sample data only.
- CI runs pytest + builds report + Docker image; `deploy.yaml` manual only;
  `weekly-report.yaml` Fridays 18:00 UTC with `fetch-data --strict` (never publishes sample data).
- Dockerfile now runs the Streamlit app (port 8501, healthcheck).
- README rewritten; `LISENCE` → `LICENSE`; Cryptopulse-AI → Market-ML in docs.

## Still to do
1. Push branch (Claude GitHub app needs write access to `Joolanda/market-ml`), open PR, check CI.
2. First real-data run: `python cli.py fetch-data` locally or "Run workflow" on weekly-report;
   check the numbers and that the README claims still hold on real data.
3. Weekly report commits to the default branch: merge this branch first.
4. AWS: one container on ECS Express Mode or Lightsail Containers (fetch data at startup or
   from S3); then replace `deploy.yaml`.
5. Optional: screenshot with real data in `docs/img/fx_weekly.png`.
