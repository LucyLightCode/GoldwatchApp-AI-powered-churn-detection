import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="GoldWatch", page_icon="🏦", layout="wide")

API = "https://goldwatchapp-ai-powered-churn-detection.onrender.com"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.main { background: linear-gradient(135deg, #0a0a0a 0%, #1a1200 100%); }

/* Header */
.header-box {
    background: linear-gradient(135deg, #1a1000, #2d1f00);
    border: 2px solid #FFD700;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 30px rgba(255,215,0,0.15);
}
.header-title {
    font-size: 2.8rem; font-weight: 900;
    background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 3px; margin: 0;
}
.header-sub {
    color: #bbb; font-size: 1rem; margin-top: 4px;
}

/* Form card */
.form-card {
    background: linear-gradient(135deg, #111, #1c1400);
    border: 1.5px solid #3d2e00;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.form-title {
    color: #FFD700; font-size: 1.1rem;
    font-weight: 700; margin-bottom: 1rem;
    border-bottom: 1px solid #3d2e00; padding-bottom: 0.5rem;
}

/* Risk results */
.result-high {
    background: linear-gradient(135deg, #2d0000, #1a0000);
    border: 2px solid #FF4B4B;
    border-radius: 14px; padding: 1.5rem;
    text-align: center; margin-top: 1rem;
}
.result-low {
    background: linear-gradient(135deg, #002d00, #001a00);
    border: 2px solid #00C851;
    border-radius: 14px; padding: 1.5rem;
    text-align: center; margin-top: 1rem;
}
.result-label { font-size: 1rem; color: #aaa; margin-bottom: 4px; }
.result-high-text { font-size: 2rem; font-weight: 900; color: #FF4B4B; }
.result-low-text  { font-size: 2rem; font-weight: 900; color: #00C851; }
.result-prob { font-size: 1.1rem; color: #ddd; margin-top: 6px; }
.action-box { background: #1a1000; border-left: 4px solid #FFD700;
              border-radius: 6px; padding: 0.8rem 1rem;
              color: #FFD700; font-size: 0.9rem; margin-top: 1rem; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1a1000, #2d1f00);
    border: 1.5px solid #FFD700;
    border-radius: 12px; padding: 1.2rem;
    text-align: center;
}
.metric-label { color: #FFD700; font-size: 0.8rem; font-weight: 600;
                text-transform: uppercase; letter-spacing: 1px; }
.metric-value { color: white; font-size: 1.8rem; font-weight: 900; margin-top: 4px; }

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 700 !important; font-size: 0.95rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <div class="header-title">🏦 GoldWatch</div>
    <div class="header-sub">AI-powered churn detection for premium banking customers</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍  Score a Customer", "📂  Batch Upload", "📊  Dashboard"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Single Customer Scorer
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="form-title">👤 Customer Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age                             = st.number_input("Age",                        min_value=18, max_value=100, value=45)
        income_bracket                  = st.selectbox("Income Bracket",               ["Low", "Medium", "High"])
        region                          = st.text_input("Region",                       value="Lagos")
        has_gold_account                = st.selectbox("Has Gold Account",             [1, 0], format_func=lambda x: "Yes" if x==1 else "No")
        has_savings_account             = st.selectbox("Has Savings Account",          [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
        num_accounts                    = st.number_input("Number of Accounts",        min_value=1, max_value=20,    value=2)
        num_distinct_account_types      = st.number_input("Distinct Account Types",    min_value=1, max_value=10,    value=1)

    with col2:
        customer_tenure_days            = st.number_input("Customer Tenure (days)",    min_value=0,  max_value=10000, value=365)
        avg_net_transaction_amount_180d = st.number_input("Avg Net Txn Amount (180d)", min_value=0.0, value=10000.0,  step=500.0)
        transaction_frequency_30d       = st.number_input("Transaction Frequency (30d)", min_value=0, max_value=500, value=5)
        avg_transaction_amount          = st.number_input("Avg Transaction Amount",    min_value=0.0, value=8000.0,   step=500.0)
        number_complaints_90d           = st.number_input("Complaints (last 90 days)", min_value=0, max_value=50,   value=0)
        num_other_checking_accounts     = st.number_input("Other Checking Accounts",   min_value=0, max_value=10,   value=0)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⚡  Predict Churn Risk", use_container_width=True, type="primary")

    if predict_btn:
        payload = {
            "age": age, "income_bracket": income_bracket, "region": region,
            "has_gold_account": has_gold_account,
            "customer_tenure_days": customer_tenure_days,
            "num_accounts": num_accounts,
            "avg_net_transaction_amount_180d": avg_net_transaction_amount_180d,
            "transaction_frequency_30d": transaction_frequency_30d,
            "avg_transaction_amount": avg_transaction_amount,
            "number_complaints_90d": number_complaints_90d,
            "num_distinct_account_types": num_distinct_account_types,
            "has_savings_account": has_savings_account,
            "num_other_checking_accounts": num_other_checking_accounts,
        }
        try:
            res  = requests.post(f"{API}/predict", json=payload)
            data = res.json()
            prob = data["churn_probability"]
            risk = data["churn_risk"]

            if risk == "High":
                st.markdown(f"""
                <div class="result-high">
                    <div class="result-label">Churn Risk Level</div>
                    <div class="result-high-text">🚨 HIGH RISK</div>
                    <div class="result-prob">Churn Probability: <b>{prob*100:.1f}%</b></div>
                </div>
                <div class="action-box">
                    💡 <b>Recommended Action:</b> Trigger immediate retention campaign —
                    personal outreach, fee waiver, or product upgrade offer.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-low">
                    <div class="result-label">Churn Risk Level</div>
                    <div class="result-low-text">✅ LOW RISK</div>
                    <div class="result-prob">Churn Probability: <b>{prob*100:.1f}%</b></div>
                </div>
                <div class="action-box">
                    💡 <b>Status:</b> Customer appears stable. Continue standard engagement.
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"⚠️ Could not reach the API. Make sure FastAPI is running.\n\n{e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Batch Upload
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="form-title">📂 Upload Customer CSV</div>', unsafe_allow_html=True)
    st.caption("Upload a CSV with the same columns as the single scorer form. Download results with churn scores.")

    file = st.file_uploader("Choose a CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.success(f"✅ {len(df):,} customers loaded")
        st.dataframe(df.head(5), use_container_width=True)

        if st.button("⚡  Score All Customers", use_container_width=True, type="primary"):
            with st.spinner("Scoring customers..."):
                try:
                    file.seek(0)
                    res     = requests.post(f"{API}/predict-batch",
                                            files={"file": ("data.csv", file, "text/csv")})
                    results = pd.DataFrame(res.json())

                    high = (results["churn_risk"] == "High").sum()
                    low  = (results["churn_risk"] == "Low").sum()

                    c1, c2 = st.columns(2)
                    c1.markdown(f'<div class="metric-card"><div class="metric-label">🚨 High Risk</div><div class="metric-value" style="color:#FF4B4B">{high}</div></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div class="metric-card"><div class="metric-label">✅ Low Risk</div><div class="metric-value" style="color:#00C851">{low}</div></div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(results, use_container_width=True)

                    csv = results.to_csv(index=False).encode()
                    st.download_button("⬇️  Download Results CSV", csv,
                                       "goldwatch_results.csv", "text/csv",
                                       use_container_width=True)
                except Exception as e:
                    st.error(f"⚠️ API error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Dashboard
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="form-title">📊 Model Performance</div>', unsafe_allow_html=True)

    try:
        health = requests.get(f"{API}/health").json()

        c1, c2, c3, c4 = st.columns(4)
        for col, label, value in zip(
            [c1, c2, c3, c4],
            ["Model", "Threshold", "ROC-AUC", "Recall"],
            [health["model"], health["threshold"], "0.7007", "0.3333"]
        ):
            col.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-title">🏆 Top Churn Drivers</div>', unsafe_allow_html=True)

        drivers = pd.DataFrame({
            "Rank":    ["🥇 1st", "🥈 2nd", "🥉 3rd"],
            "Feature": ["Complaints (90d)", "Customer Tenure", "Has Savings Account"],
            "Impact":  ["🔴 Very High",     "🟠 High",         "🟡 Medium"],
            "Recommended Action": [
                "Resolve complaints within 48hrs — flag customers with 2+ complaints",
                "Intensive onboarding programme for customers under 12 months",
                "Cross-sell savings product to single-product Gold customers",
            ]
        })
        st.dataframe(drivers, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-title">📋 Model Summary</div>', unsafe_allow_html=True)

        summary = pd.DataFrame({
            "Model":               ["Logistic Regression", "Random Forest ✅"],
            "Accuracy":            ["81.50%", "92.33%"],
            "Precision (Churn)":   ["4.46%",  "6.98%"],
            "Recall (Churn)":      ["55.56%", "33.33%"],
            "F1-Score (Churn)":    ["8.26%",  "11.54%"],
            "ROC-AUC":             ["0.6479", "0.7007"],
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)

    except:
        st.warning("⚠️ API is offline. Start the FastAPI server to load the dashboard.")
