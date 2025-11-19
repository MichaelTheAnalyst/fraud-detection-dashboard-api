/**
 * API Service Layer for Fraud Detection Dashboard
 * 
 * Handles all communication with the FastAPI backend
 * 
 * Author: Masood Nazari
 * GitHub: github.com/michaeltheanalyst
 */

import axios from 'axios';

// Base API configuration
// Use production API by default, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.MODE === 'production' 
    ? 'https://fraud-detection-dashboard-api.onrender.com'
    : 'http://localhost:8000');
const API_V1 = `${API_BASE_URL}/api/v1`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_V1,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response || error);
    return Promise.reject(error);
  }
);

// ====================
// DASHBOARD ENDPOINTS
// ====================

export const dashboardAPI = {
  // Tile 1: Executive Overview
  getExecutiveOverview: (hours = 24) =>
    apiClient.get(`/dashboard/executive-overview?hours=${hours}`),

  // Tile 2: High-Risk Transactions
  getHighRiskTransactions: (limit = 50) =>
    apiClient.get(`/dashboard/high-risk-transactions?limit=${limit}`),

  // Tile 3: Fraud Velocity Heatmap
  getFraudVelocityHeatmap: (hours = 24) =>
    apiClient.get(`/dashboard/fraud-velocity-heatmap?hours=${hours}`),

  // Tile 4: Fraud Type Breakdown
  getFraudTypeBreakdown: () =>
    apiClient.get(`/dashboard/fraud-type-breakdown`),

  // Tile 7: Behavioral Anomalies
  getBehavioralAnomalies: () =>
    apiClient.get(`/dashboard/behavioral-anomalies`),

  // Tile 18: Smart Alerts
  getSmartAlerts: (hours = 24) =>
    apiClient.get(`/dashboard/smart-alerts?hours=${hours}`),
};

// ====================
// ANALYTICS ENDPOINTS
// ====================

export const analyticsAPI = {
  // Tile 5: Geo-Anomaly Hotspots
  getGeoAnomalyHotspots: () =>
    apiClient.get(`/analytics/geo-anomaly-hotspots`),

  // Tile 6: Predictive Risk Scores
  getPredictiveRiskScores: (limit = 127) =>
    apiClient.get(`/analytics/predictive-risk-scores?limit=${limit}`),

  // Tile 10: Transaction Explanation
  getTransactionExplanation: (transactionId) =>
    apiClient.get(`/analytics/transaction-explanation/${transactionId}`),

  // Tile 14: Financial Impact
  getFinancialImpact: (periodDays = 30) =>
    apiClient.get(`/analytics/financial-impact?period_days=${periodDays}`),

  // Tile 15: Customer Experience
  getCustomerExperience: () =>
    apiClient.get(`/analytics/customer-experience`),

  // Tile 16: Temporal Trends
  getTemporalTrends: (months = 12) =>
    apiClient.get(`/analytics/temporal-trends?months=${months}`),

  // Tile 17: Merchant/Channel Risk
  getMerchantChannelRisk: () =>
    apiClient.get(`/analytics/merchant-channel-risk`),
};

// ====================
// NETWORK ENDPOINTS
// ====================

export const networkAPI = {
  // Tile 3: Fraud Network Graph
  getFraudNetworkGraph: (minFraudProb = 0.6) =>
    apiClient.get(`/network/fraud-network-graph?min_fraud_prob=${minFraudProb}`),

  // Tile 9: Mule Accounts Detection
  getMuleAccounts: (minSenders = 5) =>
    apiClient.get(`/network/mule-accounts?min_senders=${minSenders}`),
};

// ====================
// MODEL ENDPOINTS
// ====================

export const modelAPI = {
  // Tile 11: Model Health
  getModelHealth: () =>
    apiClient.get(`/model/model-health`),

  // Tile 12: Confusion Matrix
  getConfusionMatrix: () =>
    apiClient.get(`/model/confusion-matrix`),

  // Tile 13: Feature Importance
  getFeatureImportance: () =>
    apiClient.get(`/model/feature-importance`),
};

// ====================
// SYSTEM ENDPOINTS
// ====================

export const systemAPI = {
  // Health Check
  getHealth: () =>
    axios.get(`${API_BASE_URL}/health`),

  // API Info
  getApiInfo: () =>
    axios.get(`${API_BASE_URL}/`),
};

// Export combined API object
export const api = {
  dashboard: dashboardAPI,
  analytics: analyticsAPI,
  network: networkAPI,
  model: modelAPI,
  system: systemAPI,
};

export default api;

