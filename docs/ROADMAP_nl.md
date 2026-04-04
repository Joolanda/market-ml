# 🚀 Cryptopulse-AI — Project Roadmap

Deze roadmap beschrijft de transformatie van `cryptopulse-ai` naar een schaalbare, modulaire en cloud-native applicatie.

---

## ✅ Phase 1 — UI & Styling Cleanup (Completed)

- External CSS file created and linked
- Reusable UI components extracted into dedicated modules
- Streamlit layout standardized
- Navigation and page structure cleaned up

---

## 🔄 Phase 2 — Data & Logic Refactor (In Progress)

### Goals
- Scheiden van UI, data en business logic
- Voorbereiden op multi-asset support
- Voorbereiden op cloud-native deployment

### Tasks
- Move data loading logic → `src/data/data_loader.py`
- Move feature engineering → `src/features/engineering.py`
- Parameterize loaders for multiple assets (BTC, ETH, GOLD, etc.)
- Standardize file naming (`asset_timeframe_raw.csv`, `asset_timeframe_features.csv`)
- Stabilize TA logic (RSI, MACD, SMA, Bollinger)
- Ensure all indicators use last valid values (NaN-safe)

---

## 🛠 Phase 3 — Rebuild Application Structure

### Goals
- Schone, modulaire app-architectuur
- Duidelijke boundaries tussen frontend en backend

### Tasks
- Rebuild Streamlit pages using new component modules
- Introduce service layer for predictions, TA, and data pipelines
- Add caching and performance improvements
- Add configuration system for assets, timeframes, and data sources

---

## ☁️ Phase 4 — Cloud-Native Deployment

### Goals
- Backend en frontend scheiden
- Deployable op Kubernetes
- Infra-as-code

### Tasks
- Create `Dockerfile.api` for backend services
- Create `Dockerfile.streamlit` for frontend
- Define Terraform infra in `infra/`
- Add Kubernetes manifests in `k8s/`
- Add CI/CD pipeline (GitHub Actions)

---

## 🔮 Phase 5 — Future Enhancements

- Real-time data ingestion pipeline
- Websocket live price updates
- Multi-asset dashboard
- TradingView-style charts
- Alerts & notifications
- User profiles & preferences

---

## 📌 Status Summary

- Phase 1: **Completed**
- Phase 2: **In Progress**
- Phase 3: **Pending**
- Phase 4: **Pending**
- Phase 5: **Future**

---

## 🧭 Vision

Cryptopulse-AI wordt een schaalbare, modulaire en professionele trading intelligence suite — gebouwd op een solide architectuur, met een strakke UI, en klaar voor cloud-native deployment.

