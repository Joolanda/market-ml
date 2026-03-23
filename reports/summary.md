# ============================
# 12. Summary of Model Results
# ============================

## Binary Classification — Candle Direction (0/1)

The binary pipeline predicts whether the next candle moves up (1) or down (0).  
All models run correctly and produce stable, realistic results for financial time‑series data.

**Key observations**
- Accuracy ranges from 0.53 to 0.57, which is typical for short‑term crypto direction prediction.
- Precision is consistently higher than recall, indicating conservative “up” predictions.
- Logistic Regression performs the weakest due to its linear nature.
- Tree‑based models (RandomForest, XGBoost, LightGBM) perform better and more consistently.
- Confusion matrices are correct 2×2, confirming the pipeline is fully binary.

**Conclusion**  
The binary pipeline is robust, consistent, and suitable for capstone‑level evaluation.  
LightGBM performs particularly well in this setting.

---

## Multiclass Classification — Trend Labels (5 classes)

The multiclass pipeline predicts five trend categories (strong down, mild down, neutral, mild up, strong up).  
After remapping labels from −2…2 to 0…4, all models run without errors.

**Key observations**
- Accuracy is around 0.36–0.37, which is realistic for 5‑class crypto trend prediction.
- Macro‑F1 scores are low (around 0.20), reflecting the difficulty of distinguishing minority classes.
- Weighted‑F1 scores are higher (around 0.31–0.32), showing class imbalance effects.
- XGBoost performs slightly better than RandomForest and Logistic Regression.
- LightGBM is excluded from multiclass for now due to objective configuration requirements.

**Conclusion**  
The multiclass pipeline is stable and provides a solid baseline for trend prediction.  
XGBoost is currently the strongest performer in this setting.

---

## Overall Conclusions

- Both binary and multiclass pipelines are now fully functional, separated, and stable.
- Results are realistic for financial time‑series forecasting and show no signs of overfitting.
- Outputs have been saved to:
  - `results_binary.csv`
  - `results_multiclass.csv`
- The codebase is clean, modernized, and ready for further development.

---

