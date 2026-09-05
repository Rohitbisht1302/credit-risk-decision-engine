from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(title="Credit Risk Underwriting API")

# Load trained ML model
model = joblib.load('model.joblib')

class LoanRequest(BaseModel):
    monthly_income: float = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=900)
    existing_emis: float = Field(..., ge=0)
    requested_amount: float = Field(..., gt=0)
    tenure_months: int = Field(..., ge=6, le=84)

@app.get("/")
def home():
    return {"status": "API is running"}

@app.post("/evaluate")
def evaluate_loan(data: LoanRequest):
    # 1. Calculate FOIR (Fixed Obligation to Income Ratio)
    foir = (data.existing_emis / data.monthly_income) * 100

    # Hard Rule Checks
    if data.credit_score < 650:
        return {
            "status": "REJECTED",
            "reason": "Credit score below minimum required threshold (650)",
            "foir_pct": round(foir, 2)
        }

    if foir > 50.0:
        return {
            "status": "REJECTED",
            "reason": "FOIR exceeds maximum threshold of 50%",
            "foir_pct": round(foir, 2)
        }

    # 2. ML Risk Scoring
    features = pd.DataFrame([{
        'monthly_income': data.monthly_income,
        'credit_score': data.credit_score,
        'existing_emis': data.existing_emis,
        'requested_amount': data.requested_amount,
        'tenure_months': data.tenure_months
    }])
    
    default_prob = model.predict_proba(features)[0][1]

    # 3. Calculate EMI
    annual_rate = 12.0  # 12% annual interest
    r = (annual_rate / 12) / 100
    n = data.tenure_months
    emi = (data.requested_amount * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1)

    return {
        "status": "APPROVED",
        "foir_pct": round(foir, 2),
        "calculated_emi": round(emi, 2),
        "default_risk_score": round(default_prob, 3),
        "interest_rate_pct": annual_rate
    }