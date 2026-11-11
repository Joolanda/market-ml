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

## Done in this branch (work in progress, not yet tested end-to-end)
- `.gitignore`: only top-level `/data/` ignored (before, `data/` also hid `src/data/` and
  `streamlit_app/data/`, which is why the app did not start from a fresh clone).
- `src/config/assets.py` – asset registry + FRED rate series.
- `src/data/sample.py`, `src/data/sources.py`, `src/data/data_loader.py` – data layer.
- `streamlit_app/data/live_features.py`, `feature_loader.py` – missing modules restored,
  with offline fallback.
- `streamlit_app/logic/ta_logic.py` – missing `import pandas` (all indicators showed "No data").
- `src/fx/weekly.py` – weekly features/targets incl. rate differential (with publication lag).
- `src/fx/models.py` – logistic / ridge / HAR-vol models + walk-forward + evaluation.

## Still to do (day 1 plan)
1. `src/fx/report.py` – Markdown weekly report per market + track record; CLI commands
   `fetch-data`, `fx-weekly`, `fx-eval` in `cli.py`.
2. Streamlit page "FX Weekly" (asset selector, chart with 80% range, report text);
   remove debug output from `overview.py`; `predictions.py` must not crash without 15m CSV.
3. Tests (`tests/test_fx_weekly.py`): no look-ahead in features, walk-forward trains only on
   past weeks, report renders for all assets, app pages import.
4. CI: run pytest; `deploy.yaml` → manual trigger only (EKS cluster does not exist, fails on
   every push); new scheduled `weekly-report.yaml` (Fri 18:00 UTC: fetch data, build report, commit).
5. README rewrite with the story above; fix `LISENCE` → `LICENSE`; roadmap name.
6. Push: the Claude GitHub app has no write access to `Joolanda/market-ml` yet
   (GitHub → Settings → Applications → Claude → Configure).
