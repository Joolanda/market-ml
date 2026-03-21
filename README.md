# Market‑ML — Modular Machine Learning Pipeline

A clean, modular and scalable machine learning architecture designed for experimentation, model comparison and future UI integration.  
This project provides a structured foundation for training, evaluating and comparing multiple ML models on market‑related datasets.

---

## 🚀 Features

- Modular ML architecture (`src/ml/`)
- Multiple models (Random Forest, Logistic Regression, XGBoost)
- Unified training pipeline
- Extended model comparison framework
- Rich evaluation metrics (accuracy, precision, recall, F1, ROC AUC)
- Training and inference timing
- Confusion matrix support
- Streamlit‑ready output
- Notebook workspace for exploration and testing

---

## 📁 Project Structure

```
project/
│
├── src/
│   └── ml/
│       ├── models/
│       ├── training/
│       ├── evaluation/
│       ├── comparison/
│       └── utils/
│
├── scripts/
│   ├── run_comparison.py
│   └── ...
│
├── notebooks/
│   ├── exploration.ipynb
│   └── model_tests.ipynb
│
├── data/
│   └── ...
│
└── README.md
```

---

## 🧠 Model Comparison

The project includes an extended comparison module that:

- trains multiple models on the same dataset  
- computes classification metrics  
- measures training and inference time  
- generates a clean DataFrame with rankings  
- supports confusion matrices and ROC AUC  

Example usage:

```python
from src.ml.models.random_forest import RandomForestModel
from src.ml.models.logistic_regression import LogisticRegressionModel
from src.ml.models.xgboost_model import XGBoostModel
from src.ml.comparison.compare import compare_models

models = {
    "RandomForest": RandomForestModel(),
    "LogisticRegression": LogisticRegressionModel(),
    "XGBoost": XGBoostModel(),
}

df = compare_models(models, X, y)
print(df)
```

---

## 📊 Notebooks

Two notebooks are included:

- **exploration.ipynb** — dataset exploration and EDA  
- **model_tests.ipynb** — model training, evaluation and comparison  

These notebooks are intended for experimentation and analysis.

---

## 🖥️ Streamlit UI (planned)

A lightweight UI will allow users to:

- select a model  
- train and evaluate it  
- view metrics and confusion matrices  
- compare models interactively  

---

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the comparison

```bash
python scripts/run_comparison.py
```

---

## 📌 Roadmap

- [ ] Streamlit UI  
- [ ] Feature importance visualizations  
- [ ] ROC curve plots  
- [ ] Model registry  
- [ ] Hyperparameter tuning  
- [ ] Automated reporting  

---

## 🤝 Contributing

This project is part of a learning and experimentation environment.  
Contributions, ideas and improvements are welcome.

---

## 📄 License

MIT License.
