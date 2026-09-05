import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Fintech Credit Decisioning Portal", 
    page_icon="💳", 
    layout="wide"
)

# Custom CSS for Modern Fintech Styling
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 24px; border-radius: 12px; color: white; margin-bottom: 25px;">
        <h2 style="margin:0; color: #f8fafc;">💳 Digital Lending Underwriting Portal</h2>
        <p style="margin:5px 0 0 0; color: #94a3b8; font-size: 14px;">Automated Credit Evaluation & Risk Assessment Engine</p>
    </div>
""", unsafe_allow_html=True)

# Layout Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Applicant Parameters")
    monthly_income = st.number_input("Monthly Income (INR)", min_value=10000, value=75000, step=5000)
    credit_score = st.slider("Credit Score (CIBIL)", min_value=300, max_value=850, value=740)
    existing_emis = st.number_input("Existing Monthly EMIs (INR)", min_value=0, value=12000, step=2000)
    requested_amount = st.number_input("Requested Loan Amount (INR)", min_value=10000, value=300000, step=10000)
    tenure_months = st.selectbox("Tenure (Months)", options=[12, 24, 36, 48, 60], index=2)
    
    submit_btn = st.button("Evaluate Application")

with col2:
    st.subheader("🎯 Underwriting Decision")
    
    if submit_btn:
        payload = {
            "monthly_income": monthly_income,
            "credit_score": credit_score,
            "existing_emis": existing_emis,
            "requested_amount": requested_amount,
            "tenure_months": tenure_months
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/evaluate", json=payload)
            result = response.json()
            
            if result.get("status") == "APPROVED":
                st.success("✅ LOAN APPLICATION APPROVED")
                
                m1, m2 = st.columns(2)
                with m1:
                    st.metric(label="Calculated Monthly EMI", value=f"₹ {result['calculated_emi']:,}")
                    st.metric(label="FOIR Ratio", value=f"{result['foir_pct']}%")
                with m2:
                    st.metric(label="Interest Rate (P.A.)", value=f"{result['interest_rate_pct']}%")
                    st.metric(label="ML Risk Score", value=f"{result['default_risk_score']}")
                
                st.info("ℹ️ Applicant satisfies FOIR limits (<50%) and credit score eligibility benchmarks.")
                
            else:
                st.error("❌ LOAN APPLICATION REJECTED")
                st.warning(f"**Underwriting Policy Rejection:** {result.get('reason')}")
                st.metric(label="Applicant FOIR Ratio", value=f"{result.get('foir_pct')}%")
                
        except Exception as e:
            st.error(f"Error connecting to FastAPI backend API: {e}")
    else:
        st.info("👈 Enter applicant information on the left panel and click **Evaluate Application** to trigger underwriting rules.")