const API_URL = "http://127.0.0.1:8000";

let fraudChart;

async function addTransaction() {

    const user_id = document.getElementById("user_id").value;
    const amount = document.getElementById("amount").value;
    const hour = document.getElementById("hour").value;

    const response = await fetch(`${API_URL}/add_transaction`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: parseInt(user_id),
            amount: parseFloat(amount),
            transaction_hour: parseInt(hour)
        })
    });

    const data = await response.json();
    showResult(data);
    loadDashboard();
}

function showResult(data) {

    let riskClass = "low";
    let barColor = "#22c55e";

    if (data.risk_level === "MEDIUM") {
        riskClass = "medium";
        barColor = "#facc15";
    }

    if (data.risk_level === "HIGH") {
        riskClass = "high";
        barColor = "#ef4444";
    }

    document.getElementById("result").innerHTML = `
        <h3>Risk Level: <span class="${riskClass}">${data.risk_level}</span></h3>
        <p>Risk Score: ${data.risk_score}</p>
        <p>ML Probability: ${data.ml_probability}</p>
        <p>Reasons: ${data.risk_reasons.join(", ")}</p>

        <div class="risk-bar">
            <div class="risk-fill" 
                style="width:${data.risk_score}%; background:${barColor}">
            </div>
        </div>
    `;
}

async function loadDashboard() {

    const response = await fetch(`${API_URL}/dashboard`);
    const data = await response.json();

    document.getElementById("total").innerText = data.total_transactions;
    document.getElementById("high").innerText = data.high_risk_transactions;
    document.getElementById("percentage").innerText = data.fraud_percentage + "%";
    document.getElementById("avg").innerText = data.average_risk_score;

    updateChart(data.high_risk_transactions, data.total_transactions);
}

function updateChart(highRisk, total) {

    const normal = total - highRisk;

    if (!fraudChart) {
        const ctx = document.getElementById("fraudChart").getContext("2d");

        fraudChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["High Risk", "Normal"],
                datasets: [{
                    data: [highRisk, normal],
                    backgroundColor: ["#ef4444", "#22c55e"]
                }]
            }
        });
    } else {
        fraudChart.data.datasets[0].data = [highRisk, normal];
        fraudChart.update();
    }
}

loadDashboard();
setInterval(loadDashboard, 5000);
