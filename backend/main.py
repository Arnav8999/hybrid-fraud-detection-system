from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import joblib
import os
from dotenv import load_dotenv

# ==========================
# LOAD ENV VARIABLES
# ==========================

load_dotenv()

# ==========================
# FASTAPI INIT
# ==========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# LOAD ML MODEL
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model.pkl")

print("📦 Loading model from:", MODEL_PATH)

model = joblib.load(MODEL_PATH)

# ==========================
# DATABASE CONNECTION
# ==========================

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ==========================
# REQUEST MODEL
# ==========================

class Transaction(BaseModel):
    user_id: int
    amount: float
    transaction_hour: int

# ==========================
# ADD TRANSACTION
# ==========================

@app.post("/add_transaction")
def add_transaction(data: Transaction):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ======================
    # ML PREDICTION
    # ======================

    features = [[data.amount, data.transaction_hour]]
    raw_probs = model.predict_proba(features)[0]
    ml_probability = float(raw_probs[1])

    risk_score = ml_probability * 50
    risk_reasons = []

    # ======================
    # RULE 1 — HIGH AMOUNT
    # ======================

    if data.amount > 50000:
        risk_score += 20
        risk_reasons.append("High transaction amount")

    # ======================
    # RULE 2 — UNUSUAL HOUR
    # ======================

    if data.transaction_hour < 6:
        risk_score += 15
        risk_reasons.append("Transaction at unusual hour")

    # ======================
    # RULE 3 — BEHAVIORAL SPIKE
    # ======================

    cursor.execute("""
        SELECT AVG(amount) as avg_amount
        FROM transactions
        WHERE user_id = %s
    """, (data.user_id,))

    result = cursor.fetchone()
    user_avg = result["avg_amount"]

    if user_avg and data.amount > user_avg * 3:
        risk_score += 25
        risk_reasons.append("Unusual spike vs user history")

    # ======================
    # RULE 4 — VELOCITY CHECK
    # ======================

    one_minute_ago = datetime.now() - timedelta(minutes=1)

    cursor.execute("""
        SELECT COUNT(*) as txn_count
        FROM transactions
        WHERE user_id = %s
        AND timestamp >= %s
    """, (data.user_id, one_minute_ago))

    velocity_result = cursor.fetchone()
    txn_count = velocity_result["txn_count"]

    if txn_count >= 3:
        risk_score += 30
        risk_reasons.append("High transaction velocity")

    # ======================
    # DETERMINE RISK LEVEL
    # ======================

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # ======================
    # INSERT INTO DATABASE
    # ======================

    cursor.execute("""
        INSERT INTO transactions
        (user_id, amount, transaction_hour, ml_probability, risk_score, risk_level, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data.user_id,
        data.amount,
        data.transaction_hour,
        ml_probability,
        risk_score,
        risk_level,
        datetime.now()
    ))

    conn.commit()
    transaction_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "transaction_id": transaction_id,
        "ml_probability": round(ml_probability, 4),
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "risk_reasons": risk_reasons
    }

# ==========================
# DASHBOARD API
# ==========================

@app.get("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM transactions")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as fraud FROM transactions WHERE risk_level = 'HIGH'")
    fraud = cursor.fetchone()["fraud"]

    cursor.execute("SELECT AVG(risk_score) as avg_risk FROM transactions")
    avg_risk = cursor.fetchone()["avg_risk"]

    fraud_ratio = (fraud / total * 100) if total > 0 else 0

    cursor.close()
    conn.close()

    return {
        "total_transactions": total,
        "high_risk_transactions": fraud,
        "fraud_percentage": round(fraud_ratio, 2),
        "average_risk_score": round(avg_risk or 0, 2)
    }
