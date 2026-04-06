# 🚀 Cryptopulse-AI — Project Roadmap

This roadmap outlines the transformation of `cryptopulse-ai` into a modular, scalable, and cloud‑native trading intelligence platform.

---

## ✅ Phase 1 — UI & Styling Cleanup (Completed)

- Moved all inline styling into a dedicated CSS file
- Linked global CSS to Streamlit application
- Extracted reusable UI components into a dedicated module
- Standardized layout and navigation structure

---

## 🔄 Phase 2 — Data & Logic Refactor (In Progress)

### Goals
- Establish clear separation between UI, data, and business logic
- Prepare the system for multi‑asset support
- Improve maintainability and testability

### Tasks
- Move data loading logic → `src/data/data_loader.py`
- Move feature engineering logic → `src/features/engineering.py`
- Parameterize loaders and logic for multiple assets (BTC, ETH, GOLD, etc.)
- Standardize file naming (`asset_timeframe_raw.csv`, `asset_timeframe_features.csv`)
- Stabilize Technical Analysis logic (RSI, MACD, SMA, Bollinger)
- Ensure indicators use last valid values (NaN‑safe)
- Clean up imports and module boundaries

---

## 🛠 Phase 3 — Application Architecture Rebuild

### Goals
- Create a clean, modular app structure
- Introduce a service layer for predictions, TA, and data pipelines
- Improve performance and caching

### Tasks
- Rebuild Streamlit pages using new component modules
- Introduce a backend service layer (API-first architecture)
- Add caching for expensive operations
- Add configuration system for assets, timeframes, and data sources

---

## ☁️ Phase 4 — Cloud‑Native Deployment

### Goals
- Separate backend and frontend into independent services
- Deploy using containerization and infrastructure‑as‑code
- Enable scalable, production‑ready deployment

### Tasks
- Create `Dockerfile.api` for backend services
- Create `Dockerfile.streamlit` for frontend
- Define infrastructure using Terraform (`infra/`)
- Add Kubernetes manifests (`k8s/`)
- Implement CI/CD pipeline (GitHub Actions)

---

## 🔮 Phase 5 — Future Enhancements

- Real‑time data ingestion pipeline
- Websocket‑based live price updates
- Multi‑asset dashboard
- TradingView‑style charts
- Alerts & notifications
- User profiles and preferences
- Backtesting engine
- Strategy builder

---

## 📌 Status Summary

- **Phase 1:** Completed  
- **Phase 2:** In Progress  
- **Phase 3:** Pending  
- **Phase 4:** Pending  
- **Phase 5:** Future  

---

## 🧭 Vision

Cryptopulse‑AI aims to become a professional, modular, and cloud‑native trading intelligence suite — combining clean architecture, a polished UI, and scalable infrastructure to support real‑time analytics and multi‑asset insights.

## 📌 Project Roadmap — High-Level Phases

🎯 Sprint 1 — TA‑engine bouwen
# RSI

# MACD

# SMA20/50/200

# Bollinger Bands

# ATR

# Volume MA

🎯 Sprint 2 — Prediction engine
# TA‑based next candle

# Later ML‑based next candle

🎯 Sprint 3 — Data structuur afronden
# src/data/

# src/features/

# multi‑asset support

🎯 Sprint 4 — Deployment
# Docker

# Terraform

# Kubernetes

🎯 Sprint 5 — Database
# TimescaleDB in Docker

# candles_raw → hypertable

# features → hypertable

# predictions → hypertable

# API endpoints voor data ingest

# Streamlit koppelen aan DB

🎯 Sprint 6 — Authentication (Keycloak)
# Keycloak in Docker

# Realm + client + roles

# Streamlit protected routes

# API protected endpoints

# Tokens + refresh flow

🎯 Sprint 7 — Deployment
# Docker Compose

# Terraform

# Kubernetes

# Ingress + TLS

# CI/CD
