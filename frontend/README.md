# 🎨 Fraud Detection Dashboard - React Frontend

**Modern, real-time fraud detection dashboard built with React, Tailwind CSS, and Recharts.**

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?logo=vite)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)

> 🌟 **Companion frontend for** [fraud-detection-dashboard-api](https://github.com/MichaelTheAnalyst/fraud-detection-dashboard-api)

---

## 📋 Overview

Interactive dashboard providing real-time visualization of fraud detection metrics, network analysis, and ML model performance.

### **✨ Features**

- ✅ **Real-time Updates** - Auto-refreshing data with React Query
- ✅ **18 Dashboard Tiles** - Comprehensive fraud monitoring
- ✅ **Beautiful Charts** - Powered by Recharts
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Type-safe** - Built with modern React patterns
- ✅ **Fast** - Powered by Vite for instant HMR

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend API running at `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

Visit **http://localhost:3000**

---

## 📦 Project Structure

```
frontend/
├── public/                    # Static assets
├── src/
│   ├── components/
│   │   ├── shared/           # Reusable components (Card, Badge, etc.)
│   │   └── tiles/            # Dashboard tile components
│   ├── hooks/
│   │   └── useApi.js         # Custom React Query hooks
│   ├── services/
│   │   └── api.js            # API service layer
│   ├── utils/
│   │   └── formatters.js     # Utility functions
│   ├── App.jsx               # Main application component
│   ├── main.jsx              # Application entry point
│   └── index.css             # Global styles (Tailwind)
├── index.html
├── vite.config.js
├── tailwind.config.js
├── package.json
└── README.md
```

---

## 🎨 Dashboard Tiles

### **Implemented Tiles** ✅

1. **Executive Overview** - Real-time KPIs
2. **High-Risk Transactions** - Critical alerts feed
3. **Fraud Velocity Heatmap** - Hourly fraud rates
4. **Fraud Type Breakdown** - Pie chart distribution
5. **Financial Impact** - ROI scorecard
6. **Model Health** - ML performance metrics

### **Coming Soon** 🚧

7. Behavioral Anomalies
8. Geo-Anomaly Hotspots
9. Predictive Risk Scores
10. Fraud Network Graph
11. Temporal Trends
12. Merchant/Channel Risk Matrix
13. Confusion Matrix
14. Smart Alerts Feed
15-18. Additional analytics tiles

---

## 🎯 Key Components

### **API Integration** (`src/services/api.js`)
```javascript
import { api } from './services/api';

// Fetch executive overview
const data = await api.dashboard.getExecutiveOverview(24);
```

### **React Query Hooks** (`src/hooks/useApi.js`)
```javascript
import { useExecutiveOverview } from './hooks/useApi';

function MyComponent() {
  const { data, isLoading, error } = useExecutiveOverview(24);
  // Use the data
}
```

### **Formatters** (`src/utils/formatters.js`)
```javascript
import { formatCurrency, formatPercentage } from './utils/formatters';

formatCurrency(125000);      // "$125,000"
formatPercentage(4.2);       // "4.2%"
```

---

## 🎨 Styling

### **Tailwind CSS**
Custom theme with fraud detection color palette:
- **Primary** (Blue) - Information & actions
- **Danger** (Red) - Critical alerts & fraud
- **Warning** (Amber) - High-priority items
- **Success** (Green) - Positive metrics

### **Custom Components**
Pre-styled components in `src/components/shared/`:
- `Card` - Container for tiles
- `StatCard` - KPI display cards
- `Badge` - Status indicators
- `RiskBadge` - Risk level badges

---

## 📊 Data Visualization

### **Recharts Library**
Used for charts and graphs:
- Bar charts (Fraud Velocity)
- Pie charts (Fraud Types)
- Line charts (Temporal Trends)
- Area charts (Financial Impact)

### **Example Usage**
```jsx
import { BarChart, Bar, XAxis, YAxis } from 'recharts';

<BarChart data={chartData}>
  <Bar dataKey="fraud_rate" fill="#0ea5e9" />
</BarChart>
```

---

## ⚙️ Configuration

### **Environment Variables** (`.env`)
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Fraud Detection Dashboard
VITE_REFRESH_INTERVAL_FAST=10000
```

### **API Base URL**
Update in `.env` for different environments:
- Development: `http://localhost:8000`
- Production: `https://api.yourdomain.com`

---

## 🚀 Build & Deploy

### **Development**
```bash
npm run dev          # Start dev server
npm run lint         # Run ESLint
```

### **Production Build**
```bash
npm run build        # Build for production
npm run preview      # Preview production build
```

### **Deployment**

#### **Vercel** (Recommended)
```bash
npm install -g vercel
vercel
```

#### **Netlify**
```bash
npm run build
# Upload 'dist' folder to Netlify
```

#### **Docker**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

---

## 🔧 Development Guide

### **Adding a New Tile**

1. **Create Component** (`src/components/tiles/MyTile.jsx`)
```jsx
import React from 'react';
import { Card, CardHeader } from '../shared/Card';
import { useMyData } from '../../hooks/useApi';

export const MyTile = () => {
  const { data, isLoading } = useMyData();
  
  return (
    <Card loading={isLoading}>
      <CardHeader title="My Tile" icon={MyIcon} />
      {/* Your content */}
    </Card>
  );
};
```

2. **Add API Hook** (`src/hooks/useApi.js`)
```javascript
export const useMyData = () => {
  return useQuery({
    queryKey: ['my-data'],
    queryFn: async () => {
      const { data } = await api.endpoint.getMyData();
      return data;
    },
  });
};
```

3. **Import in App** (`src/App.jsx`)
```jsx
import MyTile from './components/tiles/MyTile';

// Add to dashboard
<MyTile />
```

---

## 📱 Responsive Design

Dashboard adapts to all screen sizes:
- **Desktop** (1920px+) - Full 3-column grid
- **Laptop** (1024px+) - 2-column grid
- **Tablet** (768px+) - 2-column grid
- **Mobile** (< 768px) - Single column stack

---

## 🎨 Customization

### **Colors**
Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: { ... },
      danger: { ... },
    }
  }
}
```

### **Refresh Intervals**
Edit in `.env` or `src/hooks/useApi.js`:
```javascript
refetchInterval: 30000  // 30 seconds
```

---

## 🐛 Troubleshooting

### **API Connection Errors**
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify CORS settings in backend
# Update BACKEND_CORS_ORIGINS in backend/config.py
```

### **Build Errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### **Chart Not Rendering**
- Check data format matches Recharts expectations
- Verify ResponsiveContainer parent has defined height

---

## 🔗 Related Links

- **Backend API**: https://github.com/MichaelTheAnalyst/fraud-detection-dashboard-api
- **Live Demo**: Coming soon
- **Documentation**: See API_QUICK_REFERENCE.md in backend

---

## 📄 License

MIT License - See LICENSE file

---

## 👨‍💻 Author

**Masood Nazari**  
Business Intelligence Analyst | Data Science | AI | Clinical Research

📧 Email: M.Nazari@soton.ac.uk  
🌐 Portfolio: https://michaeltheanalyst.github.io/  
💼 LinkedIn: [linkedin.com/in/masood-nazari](https://linkedin.com/in/masood-nazari)  
🔗 GitHub: [github.com/michaeltheanalyst](https://github.com/michaeltheanalyst)

---

## 🙏 Acknowledgments

- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **React Query** - Data fetching
- **Lucide React** - Icons

---

**Built with ❤️ for fraud detection excellence!** 🚀

