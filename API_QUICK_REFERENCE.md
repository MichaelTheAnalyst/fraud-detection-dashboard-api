# 🚀 API Quick Reference Guide

## Start Server

```bash
# Method 1: Using the startup script
python start_server.py

# Method 2: Direct uvicorn command
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## API Base URL
```
http://localhost:8000/api/v1
```

---

## 📊 Dashboard Endpoints

### Executive Overview (Tile 1)
```bash
GET /api/v1/dashboard/executive-overview?hours=24

Response:
{
  "fraud_amount_today": 127500.50,
  "fraud_rate_24h": 4.2,
  "fraud_rate_change": 0.6,
  "blocked_amount": 2100000.00,
  "avg_detection_time": 1.2,
  "alerts_pending": 47
}
```

### High-Risk Transactions (Tile 2)
```bash
GET /api/v1/dashboard/high-risk-transactions?limit=10

Returns: List of critical alerts with transaction details
```

### Fraud Velocity Heatmap (Tile 3)
```bash
GET /api/v1/dashboard/fraud-velocity-heatmap?hours=24

Returns: Hourly fraud rates with spike detection
```

### Fraud Type Breakdown (Tile 4)
```bash
GET /api/v1/dashboard/fraud-type-breakdown

Returns: Fraud distribution by type with trends
```

### Behavioral Anomalies (Tile 7)
```bash
GET /api/v1/dashboard/behavioral-anomalies

Returns: Detected anomaly patterns
```

### Smart Alerts (Tile 18)
```bash
GET /api/v1/dashboard/smart-alerts?hours=24

Returns: Categorized alerts (critical, warning, info)
```

---

## 🔍 Analytics Endpoints

### Geo-Anomaly Hotspots (Tile 5)
```bash
GET /api/v1/analytics/geo-anomaly-hotspots

Returns: High-risk location corridors, impossible travel
```

### Predictive Risk Scores (Tile 6)
```bash
GET /api/v1/analytics/predictive-risk-scores?limit=127

Returns: Accounts at risk in next 24 hours
```

### Financial Impact (Tile 14)
```bash
GET /api/v1/analytics/financial-impact?period_days=30

Response:
{
  "fraud_prevented": 8700000,
  "fraud_losses": 487000,
  "prevention_costs": 210000,
  "net_savings": 7900000,
  "roi_percentage": 3761
}
```

### Customer Experience (Tile 15)
```bash
GET /api/v1/analytics/customer-experience

Returns: User satisfaction metrics
```

### Temporal Trends (Tile 16)
```bash
GET /api/v1/analytics/temporal-trends?months=12

Returns: Historical trends + 30-day forecast
```

### Merchant/Channel Risk (Tile 17)
```bash
GET /api/v1/analytics/merchant-channel-risk

Returns: Risk matrix by channel × category
```

### Transaction Explanation (Tile 10)
```bash
GET /api/v1/analytics/transaction-explanation/T100000

Response:
{
  "transaction_id": "T100000",
  "fraud_probability": 0.92,
  "feature_importances": [...],
  "explanation": "Transaction flagged due to: Velocity Score, Geo Anomaly...",
  "recommended_action": "BLOCK and request verification"
}
```

---

## 🕸️ Network Analysis

### Fraud Network Graph (Tile 3)
```bash
GET /api/v1/network/fraud-network-graph?min_fraud_prob=0.6

Returns: Nodes, edges, and detected fraud rings
```

### Money Mule Detection (Tile 9)
```bash
GET /api/v1/network/mule-accounts?min_senders=5

Returns: Accounts with money laundering patterns
```

---

## 📈 Model Monitoring

### Model Health (Tile 11)
```bash
GET /api/v1/model/model-health

Response:
{
  "current_metrics": {
    "precision": 0.942,
    "recall": 0.878,
    "f1_score": 0.909
  },
  "data_drift_status": "LOW",
  "recommendation": "Model performing well"
}
```

### Confusion Matrix (Tile 12)
```bash
GET /api/v1/model/confusion-matrix

Response:
{
  "true_positive": 4234,
  "true_negative": 94789,
  "false_positive": 234,
  "false_negative": 567,
  "false_positive_rate": 0.0025
}
```

### Feature Importance (Tile 13)
```bash
GET /api/v1/model/feature-importance

Returns: Global feature importance rankings
```

---

## 🏥 System Endpoints

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "data_loaded": true,
  "data_info": {
    "rows": 5000000,
    "fraud_count": 179553
  }
}
```

### API Information
```bash
GET /

Returns: API metadata and available endpoints
```

---

## 🎯 Common Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hours` | int | 24 | Time window in hours |
| `limit` | int | varies | Max results to return |
| `min_fraud_prob` | float | 0.6 | Minimum fraud probability |
| `period_days` | int | 30 | Analysis period in days |
| `min_transactions` | int | 3 | Min transactions for connections |

---

## 🔥 Quick Test Commands

### Test All Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Executive overview
curl http://localhost:8000/api/v1/dashboard/executive-overview

# High-risk transactions
curl http://localhost:8000/api/v1/dashboard/high-risk-transactions

# Fraud network
curl http://localhost:8000/api/v1/network/fraud-network-graph

# Model health
curl http://localhost:8000/api/v1/model/model-health

# Financial impact
curl http://localhost:8000/api/v1/analytics/financial-impact
```

### Using HTTPie (prettier output)
```bash
# Install: pip install httpie

http GET localhost:8000/api/v1/dashboard/executive-overview
http GET localhost:8000/api/v1/analytics/financial-impact period_days==30
```

### Using Python
```python
import requests

# Get executive overview
response = requests.get('http://localhost:8000/api/v1/dashboard/executive-overview')
data = response.json()
print(f"Fraud Rate: {data['fraud_rate_24h']}%")

# Get high-risk transactions
response = requests.get('http://localhost:8000/api/v1/dashboard/high-risk-transactions?limit=5')
alerts = response.json()
print(f"Critical Alerts: {len(alerts['critical_alerts'])}")
```

### Using JavaScript/Fetch
```javascript
// Get financial impact
fetch('http://localhost:8000/api/v1/analytics/financial-impact')
  .then(res => res.json())
  .then(data => {
    console.log(`ROI: ${data.roi_percentage}%`);
    console.log(`Net Savings: $${data.net_savings}`);
  });
```

---

## 📱 Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 404 | Not Found (e.g., transaction ID) |
| 422 | Validation Error (invalid parameters) |
| 500 | Internal Server Error |

---

## 💡 Pro Tips

1. **Interactive Testing**: Visit http://localhost:8000/docs for Swagger UI
2. **Response Times**: Check `X-Process-Time` header for performance
3. **Caching**: First request slower (data loading), subsequent requests fast
4. **Pagination**: Use `limit` parameter for large result sets
5. **Filtering**: Combine parameters for precise queries

---

## 🎨 Frontend Integration Examples

### React Hook
```javascript
import { useState, useEffect } from 'react';

function useFraudDashboard() {
  const [overview, setOverview] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch('http://localhost:8000/api/v1/dashboard/executive-overview');
      const data = await res.json();
      setOverview(data);
    };
    
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5s
    return () => clearInterval(interval);
  }, []);
  
  return overview;
}
```

### Vue.js Component
```javascript
export default {
  data() {
    return {
      fraudRate: 0,
      alerts: 0
    }
  },
  async mounted() {
    const response = await fetch('http://localhost:8000/api/v1/dashboard/executive-overview');
    const data = await response.json();
    this.fraudRate = data.fraud_rate_24h;
    this.alerts = data.alerts_pending;
  }
}
```

---

## 🐛 Troubleshooting

### Data Not Loading?
```bash
# Check if CSV file exists
ls financial_fraud_detection_dataset.csv

# Check health endpoint
curl http://localhost:8000/health
```

### Slow Responses?
- First request loads data (expect 5-10 seconds)
- Subsequent requests are cached (< 1 second)
- Consider implementing Redis for production

### CORS Issues?
- Update `BACKEND_CORS_ORIGINS` in `backend/config.py`
- Add your frontend URL to allowed origins

---

**Happy Fraud Hunting! 🕵️‍♂️**

---

## 👨‍💻 **Author**

**Masood Nazari**  
Business Intelligence Analyst | Data Science | AI | Clinical Research

📧 Email: M.Nazari@soton.ac.uk  
🌐 Portfolio: https://michaeltheanalyst.github.io/  
💼 LinkedIn: [linkedin.com/in/masood-nazari](https://linkedin.com/in/masood-nazari)  
🔗 GitHub: [github.com/michaeltheanalyst](https://github.com/michaeltheanalyst)

