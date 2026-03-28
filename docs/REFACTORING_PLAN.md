# Refactoring Project: Kanban Board

This board tracks the progress of refactoring the `cryptopulse-ai` application into a scalable, cloud-native structure.

| To Do | In Progress | Done |
| :--- | :--- | :--- |
| **Step 1: Handle CSS** | | |
| ↳ Create a separate CSS file for styling. | | |
| ↳ Link the new CSS file to the main application. | | |
| **Step 2: Move Reusable UI Components** | | |
| ↳ Identify all reusable UI elements. | | |
| ↳ Move reusable UI components into a dedicated module. | | |
| **Step 3: Move the "Brains" (Data & Logic)** | | |
| ↳ Relocate data processing logic to `src/data/data_loader.py`. | | |
| ↳ Move feature engineering logic to `src/features/engineering.py`. | | |
| ↳ Parameterize functions to accept different assets. | | |
| ↳ Standardize data file naming (e.g., `gold_1h_raw.csv`). | | |
| **Step 4: Rebuild & Deploy** | | |
| ↳ Rebuild app pages using new components. | | |
| ↳ Create `Dockerfile.api` for the backend. | | |
| ↳ Create `Dockerfile.streamlit` for the front-end. | | |
| ↳ Define cloud infrastructure with Terraform in `infra/`. | | |
| ↳ Configure Kubernetes in `k8s/` to manage containers. | | |