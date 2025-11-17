# 🚀 Quick Start Guide - Fraud Detection Dashboard Frontend

## Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This will install:
- React 18.2.0
- Vite 5.0 (Fast build tool)
- Tailwind CSS 3.4 (Styling)
- Recharts 2.10 (Charts)
- Axios 1.6 (API calls)
- React Query 5.17 (Data fetching)
- Lucide React (Icons)

## Step 2: Start Backend API

Make sure your backend is running first:

```bash
# In the project root directory
python start_server.py

# Or manually:
uvicorn backend.main:app --reload
```

Backend should be running at: **http://localhost:8000**

## Step 3: Start Frontend

```bash
# In the frontend directory
npm run dev
```

Frontend will start at: **http://localhost:3000**

## Step 4: Open in Browser

Visit **http://localhost:3000** 

You should see:
- ✅ Executive Overview with 5 KPI cards
- ✅ High-Risk Transactions feed
- ✅ Fraud Velocity Heatmap (bar chart)
- ✅ Fraud Type Breakdown (pie chart)
- ✅ Financial Impact scorecard
- ✅ Model Health dashboard

---

## 📁 Project Structure Overview

```
frontend/
├── src/
│   ├── components/
│   │   ├── shared/
│   │   │   ├── Card.jsx         ✅ Reusable card component
│   │   │   └── Badge.jsx        ✅ Status badges
│   │   └── tiles/
│   │       ├── ExecutiveOverview.jsx       ✅ Tile 1
│   │       ├── HighRiskTransactions.jsx    ✅ Tile 2
│   │       ├── FraudVelocityHeatmap.jsx    ✅ Tile 3
│   │       ├── FraudTypeBreakdown.jsx      ✅ Tile 4
│   │       ├── FinancialImpact.jsx         ✅ Tile 14
│   │       └── ModelHealth.jsx             ✅ Tile 11
│   ├── hooks/
│   │   └── useApi.js            ✅ React Query hooks for all endpoints
│   ├── services/
│   │   └── api.js               ✅ Axios API service layer
│   ├── utils/
│   │   └── formatters.js        ✅ Currency, percentage, date formatters
│   ├── App.jsx                  ✅ Main dashboard layout
│   ├── main.jsx                 ✅ React entry point
│   └── index.css                ✅ Tailwind styles
├── package.json                 ✅ Dependencies
├── vite.config.js               ✅ Vite configuration
├── tailwind.config.js           ✅ Tailwind theme
└── README.md                    ✅ Full documentation
```

---

## ✅ What's Implemented

### **Core Infrastructure**
- ✅ React 18 with Vite (lightning-fast HMR)
- ✅ Tailwind CSS with custom theme
- ✅ React Query for data fetching
- ✅ Axios API client with interceptors
- ✅ Custom hooks for all API endpoints
- ✅ Utility functions for formatting
- ✅ Responsive grid layout
- ✅ Auto-refresh functionality

### **Dashboard Tiles (6 of 18)**
- ✅ **Tile 1**: Executive Overview - 5 KPI cards
- ✅ **Tile 2**: High-Risk Transactions - Alert feed
- ✅ **Tile 3**: Fraud Velocity Heatmap - Bar chart
- ✅ **Tile 4**: Fraud Type Breakdown - Pie chart
- ✅ **Tile 14**: Financial Impact - ROI scorecard
- ✅ **Tile 11**: Model Health - Performance metrics

### **Shared Components**
- ✅ Card, CardHeader, StatCard
- ✅ Badge, RiskBadge
- ✅ Loading states
- ✅ Error handling

---

## 🎯 Next Steps

### **Add Remaining Tiles** (12 more)

Create these tiles following the same pattern:

1. **Tile 5**: Geo-Anomaly Hotspots
2. **Tile 6**: Predictive Risk Scores
3. **Tile 7**: Behavioral Anomalies
4. **Tile 8**: Account Deep Dive
5. **Tile 9**: Money Mule Detection
6. **Tile 10**: Transaction Explanation
7. **Tile 12**: Confusion Matrix
8. **Tile 13**: Feature Importance
9. **Tile 15**: Customer Experience
10. **Tile 16**: Temporal Trends
11. **Tile 17**: Merchant/Channel Risk
12. **Tile 18**: Smart Alerts Feed

### **Example: Add New Tile**

```jsx
// 1. Create component: src/components/tiles/MyNewTile.jsx
import React from 'react';
import { Card, CardHeader } from '../shared/Card';
import { useMyData } from '../../hooks/useApi';

export const MyNewTile = () => {
  const { data, isLoading } = useMyData();
  
  return (
    <Card loading={isLoading}>
      <CardHeader title="My Tile" />
      {/* Your content */}
    </Card>
  );
};

// 2. Add hook: src/hooks/useApi.js
export const useMyData = () => {
  return useQuery({
    queryKey: ['my-data'],
    queryFn: async () => {
      const { data } = await api.endpoint.getMyData();
      return data;
    },
  });
};

// 3. Import in App.jsx
import MyNewTile from './components/tiles/MyNewTile';

// Add to dashboard
<MyNewTile />
```

---

## 🎨 Customization

### **Change Colors**
Edit `tailwind.config.js`:
```javascript
colors: {
  primary: { 500: '#YOUR_COLOR' },
  danger: { 500: '#YOUR_COLOR' },
}
```

### **Change API URL**
Create `.env` file:
```bash
VITE_API_URL=http://your-api-url:8000
```

### **Adjust Refresh Rate**
Edit in `src/hooks/useApi.js`:
```javascript
refetchInterval: 30000  // milliseconds
```

---

## 🐛 Troubleshooting

### **Port 3000 already in use**
```bash
# Use different port
npm run dev -- --port 3001
```

### **API connection error**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in `backend/config.py`
3. Verify `.env` has correct API_URL

### **Charts not showing**
1. Check data format in console
2. Verify ResponsiveContainer has height
3. Check Recharts import statements

---

## 📊 Features in Action

### **Auto-Refresh**
- Toggle button in header
- Updates every 10-30 seconds
- Real-time fraud monitoring

### **Responsive Design**
- Desktop: 3-column grid
- Tablet: 2-column grid
- Mobile: Single column stack

### **Loading States**
- Skeleton loading animations
- Graceful error handling
- Retry functionality

---

## 🚀 Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Deploy to Vercel
vercel

# Deploy to Netlify
# Upload 'dist' folder
```

---

## 📞 Need Help?

- **Backend Docs**: See `API_QUICK_REFERENCE.md` in project root
- **Component Examples**: Check existing tiles in `src/components/tiles/`
- **API Hooks**: All defined in `src/hooks/useApi.js`

---

## 🎉 You're Ready!

Your frontend is configured and ready to connect to the backend API. Start the servers and begin building!

```bash
# Terminal 1: Backend
python start_server.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit: **http://localhost:3000** 🚀

---

**Built by Masood Nazari** | [GitHub](https://github.com/michaeltheanalyst) | [Portfolio](https://michaeltheanalyst.github.io/)

