import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# 1. Generate Synthetic Financial Data (2,000 applicants)
np.random.seed(42)
n_samples = 2000

monthly_income = np.random.randint(20000, 150000, n_samples)
credit_score = np.random.randint(300, 850, n_samples)
existing_emis = np.random.randint(0, 40000, n_samples)
requested_amount = np.random.randint(50000, 1000000, n_samples)
tenure_months = np.random.choice([12, 24, 36, 48, 60], n_samples)

# Rule for default generation (synthetic ground truth)
foir = (existing_emis / monthly_income) * 100
is_default = np.where((credit_score < 600) | (foir > 50), 1, 0)

df = pd.DataFrame({
    'monthly_income': monthly_income,
    'credit_score': credit_score,
    'existing_emis': existing_emis,
    'requested_amount': requested_amount,
    'tenure_months': tenure_months,
    'is_default': is_default
})

# 2. Train Random Forest Model
X = df[['monthly_income', 'credit_score', 'existing_emis', 'requested_amount', 'tenure_months']]
y = df['is_default']

# Fixed the typo here: test_size=0.2
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Save Model File
joblib.dump(model, 'model.joblib')
print("Model trained and saved as 'model.joblib' successfully!")