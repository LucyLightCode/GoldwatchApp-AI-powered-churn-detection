import joblib
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import io
import os

# ── Load model & preprocessor ─────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
preprocessor = joblib.load(os.path.join(BASE_DIR, "churn_models", "preprocessor.joblib"))
model        = joblib.load(os.path.join(BASE_DIR, "churn_models", "random_forest_model.joblib"))
THRESHOLD    = 0.30

# ── 2. Define the app ─────────────────────────────────────────────────────────
app = FastAPI(
    title="GoldWatch",
    description="AI-powered churn detection system for premium banking customers",
   
)
version="1.0.0",
contact={
        "name": "Busayo Lucia Ajayi",
        "url": "https://www.linkedin.com/in/busayo-ajayi-lucia/",
    },
license_info={
        "name": "GitHub Repository",
        "url": "https://github.com/LucyLightCode/GoldwatchApp-AI-powered-churn-detection",
    }

# ── 3. Define what one customer's data looks like ────────────────────────────
class Customer(BaseModel):
    age:                          int
    income_bracket:               str   # "Low" | "Medium" | "High"
    region:                       str
    has_gold_account:             int   # 1 or 0
    customer_tenure_days:         int
    num_accounts:                 int
    avg_net_transaction_amount_180d: float
    transaction_frequency_30d:    int
    avg_transaction_amount:       float
    number_complaints_90d:        int
    num_distinct_account_types:   int
    has_savings_account:          int   # 1 or 0
    num_other_checking_accounts:  int

# ── 4. Helper: run the model on a dataframe ───────────────────────────────────
def predict(df: pd.DataFrame) -> list:
    X_processed = preprocessor.transform(df)
    probas      = model.predict_proba(X_processed)[:, 1]
    return [
        {
            "churn_probability": round(float(p), 4),
            "churn_risk":        "High" if p >= THRESHOLD else "Low",
        }
        for p in probas
    ]

# ── 5. Endpoints ──────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Union Bank Churn API is running"}


@app.post("/predict")
def predict_one(customer: Customer):
    """Score a single customer sent as JSON."""
    df = pd.DataFrame([customer.model_dump()])
    return predict(df)[0]


@app.post("/predict-batch")
def predict_batch(file: UploadFile = File(...)):
    """Score many customers — upload a CSV, get back a CSV with churn scores."""
    df      = pd.read_csv(io.BytesIO(file.file.read()))
    results = predict(df)
    df["churn_probability"] = [r["churn_probability"] for r in results]
    df["churn_risk"]        = [r["churn_risk"]        for r in results]
    return df.to_dict(orient="records")


@app.get("/health")
def health():
    return {"status": "ok", "model": "Random Forest", "threshold": THRESHOLD}
