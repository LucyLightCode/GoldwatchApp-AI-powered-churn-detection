# Union Bank Churn API

## Folder structure
```
churn_api/
├── main.py               ← the entire API (60 lines)
├── requirements.txt      ← dependencies
└── churn_models/         ← copy your saved .joblib files here
    ├── preprocessor.joblib
    └── random_forest_model.joblib
```

## Run locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload
```

The API is now live at: http://127.0.0.1:8000

## Test it

Open http://127.0.0.1:8000/docs in your browser.
FastAPI generates an interactive test page automatically — no extra tools needed.

## Endpoints

| Method | Endpoint         | What it does                        |
|--------|-----------------|-------------------------------------|
| GET    | /               | Check the API is running            |
| GET    | /health         | Model name + threshold in use       |
| POST   | /predict        | Score 1 customer (JSON input)       |
| POST   | /predict-batch  | Score many customers (CSV upload)   |

## Example JSON for /predict

```json
{
  "age": 45,
  "income_bracket": "Medium",
  "region": "Lagos",
  "has_gold_account": 1,
  "customer_tenure_days": 1200,
  "num_accounts": 2,
  "avg_net_transaction_amount_180d": 15000.0,
  "transaction_frequency_30d": 4,
  "avg_transaction_amount": 8000.0,
  "number_complaints_90d": 2,
  "num_distinct_account_types": 2,
  "has_savings_account": 0,
  "num_other_checking_accounts": 1
}
```

Expected response:
```json
{
  "churn_probability": 0.3812,
  "churn_risk": "High"
}
```
