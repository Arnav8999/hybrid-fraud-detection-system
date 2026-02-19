from datetime import datetime, timedelta
import numpy as np


def calculate_risk(data, model, conn):

    cursor = conn.cursor()

    # -------------------------
    # 1️⃣ AUTO DETECT TIME
    # -------------------------
    current_hour = datetime.now().hour

    # ML prediction
    features = np.array([[data.amount, current_hour]])
    ml_prob = model.predict_proba(features)[0][1]

    risk_score = ml_prob
    reasons = []

    if ml_prob > 0.5:
        reasons.append("High ML fraud probability")

    # -------------------------
    # 2️⃣ Large Amount Rule
    # -------------------------
    if data.amount > 100000:
        risk_score += 0.2
        reasons.append("Large transaction amount")

    # -------------------------
    # 3️⃣ Night Transaction Rule
    # -------------------------
    if current_hour < 5:
        risk_score += 0.15
        reasons.append("Transaction at unusual hour")

    # -------------------------
    # 4️⃣ Behavioral Spike Rule
    # -------------------------
    cursor.execute("""
        SELECT AVG(amount)
        FROM transactions
        WHERE user_id = %s
    """, (data.user_id,))

    avg_amount = cursor.fetchone()[0]

    if avg_amount and data.amount > avg_amount * 3:
        risk_score += 0.25
        reasons.append("Unusual spike vs user history")

    # -------------------------
    # 5️⃣ Velocity Detection
    # -------------------------
    one_minute_ago = datetime.now() - timedelta(minutes=1)

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = %s
        AND timestamp >= %s
    """, (data.user_id, one_minute_ago))

    recent_count = cursor.fetchone()[0]

    if recent_count >= 3:
        risk_score += 0.3
        reasons.append("Multiple rapid transactions (velocity risk)")

    # -------------------------
    # Risk Level Mapping
    # -------------------------
    if risk_score < 0.3:
        risk_level = "Low Risk"
    elif risk_score < 0.6:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return ml_prob, risk_score, risk_level, reasons
