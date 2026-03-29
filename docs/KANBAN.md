# 🗂️ Refactoring Project: Kanban Board

This board tracks the progress of refactoring the `cryptopulse-ai` application into a scalable, modular, and cloud‑native architecture.

---

## 📌 Kanban Overview

| To Do | In Progress | Done |
| :--- | :--- | :--- |
| **Step 1: Handle CSS** |  | ✔️ |
| ↳ Create a separate CSS file for styling |  | ✔️ |
| ↳ Link the new CSS file to the main application |  | ✔️ |
| **Step 2: Move Reusable UI Components** |  | ✔️ |
| ↳ Identify all reusable UI elements |  | ✔️ |
| ↳ Move reusable UI components into a dedicated module |  | ✔️ |
| **Step 3: Move the “Brains” (Data & Logic)** | 🔄 |  |
| ↳ Relocate data processing logic to `src/data/data_loader.py` | 🔄 |  |
| ↳ Move feature engineering logic to `src/features/engineering.py` | 🔄 |  |
| ↳ Parameterize functions to accept different assets | 🔄 |  |
| ↳ Standardize data file naming (e.g., `gold_1h_raw.csv`) | 🔄 |  |
| **Step 4: Rebuild & Deploy** |  |  |
| ↳ Rebuild app pages using new components |  |  |
| ↳ Create `Dockerfile.api` for the backend |  |  |
| ↳ Create `Dockerfile.streamlit` for the frontend |  |  |
| ↳ Define cloud infrastructure with Terraform in `infra/` |  |  |
| ↳ Configure Kubernetes in `k8s/` to manage containers |  |  |

---

## 📝 Notes

- Steps 1 and 2 are fully completed.
- Step 3 is currently in progress and partially completed (TA logic stabilized, loaders cleaned up).
- Steps 4 and beyond will begin once Step 3 is fully wrapped up.

---

## 🧭 Purpose

This Kanban board serves as the authoritative reference for the refactoring process.  
It ensures clarity, structure, and a calm, step‑by‑step workflow as the project evolves into a production‑ready architecture.
