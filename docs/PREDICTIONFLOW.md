          ┌──────────────────────┐
          │   Raw Market Data    │
          │ (Binance / CSV / DB) │
          └─────────┬────────────┘
                    │
                    ▼
        ┌──────────────────────────┐
        │  Data Loader (src/data)  │
        │ load_raw_candles()       │
        └─────────┬────────────────┘
                  │ Cleaned candles
                  ▼
      ┌────────────────────────────────────┐
      │ Feature Engineering (src/features) │
      │ engineer_features()                │ 
      └───────────┬────────────────────────┘
                  │ Feature matrix (X)
                  ▼
     ┌──────────────────────────────────┐
     │ Prediction Service (src/ml)      │
     │ load_model(asset, timeframe)     │
     │ model.predict_proba(X)           │
     └──────────────┬───────────────────┘
                    │ Probabilities
                    ▼
        ┌───────────────────────────────────┐
        │ Prediction Wrapper (src/features) │
        │ ta_next_candle_prediction()       │
        └──────────────┬────────────────────┘
                       │ Final dict
                       ▼
           ┌──────────────────────────┐
           │ Streamlit UI (pages/)    │
           │ predictions.py           │
           └──────────────────────────┘
