# 🚀 Hybrid Fraud Detection System  
### Real-Time ML + Rule Engine Risk Scoring API with Dashboard

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue)

---

## 📌 Overview

This project is a **Real-Time Hybrid Fraud Detection System** that combines:

- Machine Learning fraud prediction  
- Rule-Based behavioral risk detection  
- Velocity-based anomaly detection  
- Risk scoring engine  
- Interactive monitoring dashboard  

The system evaluates financial transactions and returns:

- ML fraud probability  
- Dynamic risk score  
- Risk level (LOW / MEDIUM / HIGH)  
- Clear risk reasons  
- Fraud analytics dashboard  

---

## 🧠 Why Hybrid Detection?

Traditional systems rely only on:

- ML models (may miss behavioral patterns)
- Static rules (may miss statistical fraud patterns)

This system combines both approaches to improve detection reliability.

---

## 🏗 System Architecture

Frontend (HTML / CSS / JS)
↓
FastAPI Backend (API Layer)
↓
Hybrid Risk Engine
├── ML Model (predict_proba)
├── High Amount Rule
├── Unusual Hour Rule
├── Behavioral Spike Rule
└── Velocity Rule (1-minute window)
↓
MySQL Database
↓
Dashboard API


---

## ⚙️ Core Features

### 🤖 Machine Learning Layer
- Trained using credit card fraud dataset
- Uses `predict_proba`
- Handles class imbalance
- Outputs fraud probability score

---

### ⚙️ Rule-Based Risk Engine

The rule engine enhances ML predictions with:

- High transaction amount detection  
- Unusual transaction hour detection  
- Behavioral spike compared to user history  
- High transaction velocity (multiple transactions within 1 minute)  

---

### 📊 Risk Scoring Logic

Final Risk Score is calculated using:

ML Probability × Weight

Rule Adjustments


Risk Levels:

| Score Range | Risk Level |
|-------------|------------|
| 0 – 39      | LOW        |
| 40 – 69     | MEDIUM     |
| 70+         | HIGH       |

---

## 📊 Dashboard API

The dashboard endpoint provides:

- Total transactions  
- High-risk transactions  
- Fraud percentage  
- Average risk score  

Endpoint:

GET /dashboard


---

## 🛠 Tech Stack

- Python  
- FastAPI  
- Scikit-learn  
- MySQL  
- HTML / CSS / JavaScript  
- Uvicorn  
- Joblib  

---

## 📂 Project Structure

backend/
main.py
database.py
scoring_engine.py

frontend/
index.html
app.js
style.css

training/
train_model.py

data_generator/
generate_data.py

model.pkl
requirements.txt
README.md


---

## 🚀 How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/hybrid-fraud-detection-system.git
cd hybrid-fraud-detection-system
2️⃣ Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Create .env File
Create a .env file in the project root:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=fraud_detection
5️⃣ Run Backend
cd backend
uvicorn main:app --reload
Open:

http://127.0.0.1:8000/docs
📌 Example API Response
{
  "transaction_id": 1348,
  "ml_probability": 1.0,
  "risk_score": 100,
  "risk_level": "HIGH",
  "risk_reasons": [
    "High transaction amount",
    "Transaction at unusual hour"
  ]
}
📈 Future Improvements
Cloud deployment (Render / AWS)

User authentication

Real-time streaming pipeline

Live charts with Chart.js

Advanced anomaly detection model

👨‍💻 Author
Arnav Singh
B.Tech Electronics & Computer Science
Machine Learning | Backend Systems | Fraud Detection

