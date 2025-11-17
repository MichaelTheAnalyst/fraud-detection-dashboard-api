# 🚀 Getting Started - Fraud Detection Dashboard Backend

## ⚡ Quick Start (60 seconds)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python start_server.py
```

### Step 3: Test the API
```bash
python test_api.py
```

### Step 4: Open Interactive Docs
Visit: **http://localhost:8000/docs**

---

## ✅ What You Have

### **18 Dashboard Tiles - All Implemented**

✅ **Tier 1: Executive Overview**
- Real-time Fraud Pulse KPIs
- High-Risk Transaction Feed
- Smart Alert System

✅ **Tier 2: Operational Command**
- Fraud Velocity Heatmap
- Fraud Type Breakdown
- Behavioral Anomaly Detection

✅ **Tier 3: Investigation**
- Fraud Network Graph
- Money Mule Detection
- Transaction Explanation (XAI)

✅ **Tier 4: Model Monitoring**
- Model Health Dashboard
- Confusion Matrix
- Feature Importance

✅ **Tier 5: Business Intelligence**
- Geo-Anomaly Hotspots
- Predictive Risk Scores
- Financial Impact Analysis
- Customer Experience Metrics
- Temporal Trends & Forecasting
- Merchant/Channel Risk Matrix

### **Production-Ready Features**

✅ FastAPI async framework  
✅ 20+ REST API endpoints  
✅ Efficient 5M+ row data processing  
✅ Comprehensive error handling  
✅ Request logging & timing  
✅ CORS configuration  
✅ API versioning  
✅ Swagger/ReDoc documentation  
✅ Type-safe Pydantic models  
✅ Network graph algorithms  
✅ Predictive analytics  
✅ Explainable AI  

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **README.md** | Complete project documentation |
| **API_QUICK_REFERENCE.md** | Quick API usage guide with examples |
| **PROJECT_STRUCTURE.md** | Architecture and code organization |
| **GETTING_STARTED.md** | This file - Quick start guide |

---

## 🔧 Configuration

### Default Settings (in `backend/config.py`):
- **Port**: 8000
- **Host**: 0.0.0.0 (all interfaces)
- **Data File**: `financial_fraud_detection_dataset.csv`
- **Cache TTL**: 300 seconds (5 minutes)
- **High Risk Threshold**: 0.75 (75% probability)

### Environment Variables (.env):
Create a `.env` file to override defaults:
```env
DEBUG=True
DATA_FILE_PATH=financial_fraud_detection_dataset.csv
HIGH_RISK_THRESHOLD=0.75
```

---

## 📊 API Endpoints Summary

### **Base URL**: `http://localhost:8000/api/v1`

#### Dashboard Endpoints
```
GET /dashboard/executive-overview
GET /dashboard/high-risk-transactions
GET /dashboard/fraud-velocity-heatmap
GET /dashboard/fraud-type-breakdown
GET /dashboard/behavioral-anomalies
GET /dashboard/smart-alerts
```

#### Analytics Endpoints
```
GET /analytics/geo-anomaly-hotspots
GET /analytics/predictive-risk-scores
GET /analytics/financial-impact
GET /analytics/customer-experience
GET /analytics/temporal-trends
GET /analytics/merchant-channel-risk
GET /analytics/transaction-explanation/{transaction_id}
```

#### Network Analysis
```
GET /network/fraud-network-graph
GET /network/mule-accounts
```

#### Model Monitoring
```
GET /model/model-health
GET /model/confusion-matrix
GET /model/feature-importance
```

---

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Executive overview
curl http://localhost:8000/api/v1/dashboard/executive-overview

# High-risk transactions
curl http://localhost:8000/api/v1/dashboard/high-risk-transactions?limit=10
```

### Automated Testing
```bash
# Run the test suite
python test_api.py
```

### Interactive Testing
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📈 Performance

**Expected Response Times** (5M row dataset):
- Health check: < 10ms
- Executive overview: ~100ms
- High-risk transactions: ~120ms
- Network graph: ~450ms
- Most endpoints: < 200ms

**First Request**: Slower (5-10s) due to data loading  
**Subsequent Requests**: Fast (< 1s) due to caching

---

## 🎨 Frontend Integration

### React Example
```javascript
// Fetch executive overview
const fetchDashboard = async () => {
  const response = await fetch(
    'http://localhost:8000/api/v1/dashboard/executive-overview'
  );
  const data = await response.json();
  console.log(`Fraud Rate: ${data.fraud_rate_24h}%`);
};
```

### Python Example
```python
import requests

# Get financial impact
response = requests.get(
    'http://localhost:8000/api/v1/analytics/financial-impact'
)
data = response.json()
print(f"ROI: {data['roi_percentage']}%")
print(f"Net Savings: ${data['net_savings']:,.2f}")
```

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 8000 is already in use
netstat -an | findstr 8000  # Windows
lsof -i :8000              # Mac/Linux

# Use different port
uvicorn backend.main:app --port 8001
```

### Data Not Loading
```bash
# Verify CSV file exists
ls financial_fraud_detection_dataset.csv

# Check file path in config
python -c "from backend.config import settings; print(settings.DATA_FILE_PATH)"

# Test health endpoint
curl http://localhost:8000/health
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify Python version (3.9+)
python --version
```

### Slow Performance
- **First Request**: Normal (data loading)
- **All Requests**: Check dataset size, consider sampling for development
- **Production**: Implement Redis caching or migrate to PostgreSQL

---

## 🚢 Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t fraud-api .
docker run -p 8000:8000 fraud-api
```

### Production (Gunicorn)
```bash
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 📝 Next Steps

### Immediate
1. ✅ Start the server: `python start_server.py`
2. ✅ Test the API: `python test_api.py`
3. ✅ Explore docs: http://localhost:8000/docs
4. ✅ Try example requests from `API_QUICK_REFERENCE.md`

### Short-term
- [ ] Build frontend dashboard (React/Vue/Angular)
- [ ] Customize alert thresholds in config
- [ ] Add authentication (JWT)
- [ ] Implement rate limiting
- [ ] Set up monitoring (Prometheus)

### Long-term
- [ ] Add Redis caching
- [ ] Migrate to PostgreSQL
- [ ] WebSocket for real-time updates
- [ ] Advanced ML models
- [ ] Microservices architecture
- [ ] Kubernetes deployment

---

## 💡 Pro Tips

1. **Development Mode**: Server auto-reloads on code changes (with `--reload`)
2. **API Docs**: Swagger UI provides interactive testing
3. **Response Times**: Check `X-Process-Time` header
4. **Data Caching**: First request slow, subsequent fast
5. **Error Details**: Set `DEBUG=True` for detailed error messages
6. **CORS**: Configure `BACKEND_CORS_ORIGINS` for your frontend

---

## 🤝 Support Resources

- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pandas Docs**: https://pandas.pydata.org/

---

## 🎯 Sample Workflow

### For Data Scientists
```bash
# Start server
python start_server.py

# Test model performance
curl http://localhost:8000/api/v1/model/model-health

# Check feature importance
curl http://localhost:8000/api/v1/model/feature-importance

# Analyze drift
# Review data_drift_status and feature_drift_alerts
```

### For Fraud Analysts
```bash
# Start server
python start_server.py

# Get high-risk transactions
curl http://localhost:8000/api/v1/dashboard/high-risk-transactions

# Investigate network
curl http://localhost:8000/api/v1/network/fraud-network-graph

# Explain specific transaction
curl http://localhost:8000/api/v1/analytics/transaction-explanation/T100000
```

### For Business Stakeholders
```bash
# Start server
python start_server.py

# Get executive overview
curl http://localhost:8000/api/v1/dashboard/executive-overview

# Check financial impact
curl http://localhost:8000/api/v1/analytics/financial-impact

# Review customer experience
curl http://localhost:8000/api/v1/analytics/customer-experience
```

---

## 📞 Need Help?

1. **Read the Docs**: Start with `README.md`
2. **Check Examples**: See `API_QUICK_REFERENCE.md`
3. **Test Endpoints**: Use Swagger UI
4. **Review Logs**: Check server console output
5. **Verify Health**: http://localhost:8000/health

---

**You're all set! Start building amazing fraud detection dashboards! 🚀**

```
   _____ _             _     _    _ _____ _____  ______ 
  / ____| |           | |   | |  | |_   _|  __ \|  ____|
 | (___ | |_ __ _ _ __| |_  | |__| | | | | |__) | |__   
  \___ \| __/ _` | '__| __| |  __  | | | |  _  /|  __|  
  ____) | || (_| | |  | |_  | |  | |_| |_| | \ \| |____ 
 |_____/ \__\__,_|_|   \__| |_|  |_|_____|_|  \_\______|
                                                        
        Fraud Detection Dashboard Backend
           Production-Ready API v1.0.0
```

