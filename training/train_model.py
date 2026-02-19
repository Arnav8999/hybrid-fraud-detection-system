import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

np.random.seed(42)

# -------------------------
# Generate Data
# -------------------------
n_samples = 5000

# Increase variance
amount = np.random.normal(60000, 60000, n_samples)
amount = np.abs(amount)

transaction_hour = np.random.randint(0, 24, n_samples)

fraud = []

for i in range(n_samples):

    # Strong fraud pattern
    if amount[i] > 120000 and transaction_hour[i] <= 6:
        fraud.append(1)

    elif amount[i] > 180000:
        fraud.append(1)

    elif transaction_hour[i] <= 4 and amount[i] > 80000:
        fraud.append(1)

    else:
        fraud.append(0)

fraud = np.array(fraud)

df = pd.DataFrame({
    "amount": amount,
    "transaction_hour": transaction_hour,
    "fraud": fraud
})

print("Fraud count:", df["fraud"].sum())
print("Fraud ratio:", df["fraud"].mean())

# -------------------------
# Train Model
# -------------------------
X = df[["amount", "transaction_hour"]]
y = df["fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("Model accuracy:", accuracy)

joblib.dump(model, "model.pkl")

print("Model retrained and saved successfully.")
