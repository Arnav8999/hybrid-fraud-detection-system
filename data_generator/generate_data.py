import mysql.connector
import random
from datetime import datetime, timedelta

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Arnav@8999",   # Your password (local use only)
    database="fraud_detection"
)

cursor = conn.cursor()

# ---------------------------
# CREATE USERS (36 USERS)
# ---------------------------
print("Creating 36 users...")

behavior_profiles = [
    "conservative",
    "medium",
    "high_spender",
    "night_active",
    "burst_user"
]

for i in range(36):
    cursor.execute("""
        INSERT INTO users (name, email)
        VALUES (%s, %s)
    """, (f"User_{i+1}", f"user{i+1}@mail.com"))

conn.commit()

# ---------------------------
# GENERATE TRANSACTIONS
# ---------------------------
print("Generating realistic transactions...")

cursor.execute("SELECT user_id FROM users")
users = cursor.fetchall()

for user in users:

    user_id = user[0]
    behavior = random.choice(behavior_profiles)

    transaction_count = random.randint(25, 40)

    for _ in range(transaction_count):

        # Behavior-based amount patterns
        if behavior == "conservative":
            amount = random.uniform(800, 3000)
            hour = random.randint(9, 20)

        elif behavior == "medium":
            amount = random.uniform(5000, 15000)
            hour = random.randint(9, 22)

        elif behavior == "high_spender":
            amount = random.uniform(20000, 50000)
            hour = random.randint(10, 23)

        elif behavior == "night_active":
            amount = random.uniform(2000, 8000)
            hour = random.randint(1, 4)

        elif behavior == "burst_user":
            amount = random.uniform(1000, 10000)
            hour = random.randint(8, 23)

        # Random timestamp in last 30 days
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 30),
            minutes=random.randint(0, 1440)
        )

        cursor.execute("""
            INSERT INTO transactions
            (user_id, amount, transaction_hour, ml_probability, risk_score, risk_level, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            round(amount, 2),
            hour,
            0.0,
            0.0,
            "Low Risk",
            timestamp
        ))

        # Burst behavior simulation
        if behavior == "burst_user" and random.random() < 0.2:
            for _ in range(random.randint(2, 5)):
                cursor.execute("""
                    INSERT INTO transactions
                    (user_id, amount, transaction_hour, ml_probability, risk_score, risk_level, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    round(amount, 2),
                    hour,
                    0.0,
                    0.0,
                    "Low Risk",
                    timestamp
                ))

conn.commit()

print("Synthetic data generation complete.")
print("36 users created successfully.")
