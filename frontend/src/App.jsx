import React, { useState, useEffect } from 'react';
import { AlertTriangle, Activity, BarChart3, Shield, RefreshCw } from 'lucide-react';
import ExecutiveOverview from './components/tiles/ExecutiveOverview';
import HighRiskTransactions from './components/tiles/HighRiskTransactions';
import FraudVelocityHeatmap from './components/tiles/FraudVelocityHeatmap';
import FraudTypeBreakdown from './components/tiles/FraudTypeBreakdown';
import FinancialImpact from './components/tiles/FinancialImpact';
import ModelHealth from './components/tiles/ModelHealth';
import { useHealthCheck } from './hooks/useApi';

/**
 * Main Fraud Detection Dashboard Application
 * 
 * Author: Masood Nazari
 * Business Intelligence Analyst | Data Science | AI | Clinical Research
 * GitHub: github.com/michaeltheanalyst
 */
function App() {
  const [autoRefresh, setAutoRefresh] = useState(true);
  const { data: healthData, error: healthError } = useHealthCheck();
  
  // Show API URL in development
  const apiUrl = import.meta.env.VITE_API_URL || 
    (import.meta.env.MODE === 'production' 
      ? 'https://fraud-detection-dashboard-api.onrender.com'
      : 'http://localhost:8000');
  
  // Keep Render API awake - ping health endpoint every 10 minutes
  useEffect(() => {
    if (import.meta.env.MODE === 'production' && apiUrl.includes('onrender.com')) {
      const keepAliveInterval = setInterval(() => {
        // Ping health endpoint to keep Render awake
        fetch(`${apiUrl}/health`)
          .then(() => console.log('✅ Keep-alive ping successful'))
          .catch(() => console.log('⚠️ Keep-alive ping failed (API may be sleeping)'));
      }, 10 * 60 * 1000); // Every 10 minutes
      
      return () => clearInterval(keepAliveInterval);
    }
  }, [apiUrl]);
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-danger-600 p-2 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Fraud Detection Dashboard
                </h1>
                <p className="text-sm text-gray-500">
                  Real-time monitoring and analytics
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              {/* System Status */}
              <div className="flex items-center gap-2">
                <div className={`h-2 w-2 rounded-full ${healthData?.status === 'healthy' ? 'bg-success-500 animate-pulse' : 'bg-danger-500'}`} />
                <span className="text-sm text-gray-600">
                  {healthData?.status === 'healthy' ? 'System Online' : 'System Degraded'}
                </span>
                {healthError && (
                  <span className="text-xs text-danger-600 ml-2" title={healthError.message}>
                    (API Error)
                  </span>
                )}
              </div>
              
              {/* API URL Debug (only in development) */}
              {import.meta.env.DEV && (
                <div className="text-xs text-gray-500" title="API URL being used">
                  API: {apiUrl.replace('https://', '').replace('http://', '').substring(0, 30)}...
                </div>
              )}
              
              {/* Auto-refresh Toggle */}
              <button
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  autoRefresh 
                    ? 'bg-success-50 text-success-700 hover:bg-success-100' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <RefreshCw className={`h-4 w-4 ${autoRefresh ? 'animate-spin-slow' : ''}`} />
                Auto-refresh: {autoRefresh ? 'ON' : 'OFF'}
              </button>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Dashboard Content */}
      <main className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="space-y-6">
          {/* Tier 1: Executive Overview */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <Activity className="h-5 w-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-900">Executive Pulse</h2>
            </div>
            <ExecutiveOverview />
          </section>
          
          {/* Tier 2: Operational Command Center */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="h-5 w-5 text-danger-600" />
              <h2 className="text-lg font-semibold text-gray-900">Operational Command</h2>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <HighRiskTransactions />
              <FraudVelocityHeatmap />
            </div>
          </section>
          
          {/* Tier 3: Analytics & Intelligence */}
          <section>
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 className="h-5 w-5 text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-900">Analytics & Intelligence</h2>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <FraudTypeBreakdown />
              <FinancialImpact />
              <ModelHealth />
            </div>
          </section>
          
          {/* More tiles can be added here */}
          <div className="card bg-primary-50 border-primary-200 p-8 text-center">
            <h3 className="text-lg font-semibold text-primary-900 mb-2">
              🚀 Dashboard Under Construction
            </h3>
            <p className="text-primary-700">
              More tiles are being added: Network Graph, Geo Hotspots, Temporal Trends, and more!
            </p>
            <p className="text-sm text-primary-600 mt-2">
              15 more visualization tiles coming soon...
            </p>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-sm text-gray-600">
              <p>Built with ❤️ by <strong>Masood Nazari</strong></p>
              <p className="text-xs text-gray-500 mt-1">
                Business Intelligence Analyst | Data Science | AI | Clinical Research
              </p>
            </div>
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <a 
                href="https://michaeltheanalyst.github.io/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-primary-600 transition-colors"
              >
                Portfolio
              </a>
              <span>•</span>
              <a 
                href="https://linkedin.com/in/masood-nazari" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-primary-600 transition-colors"
              >
                LinkedIn
              </a>
              <span>•</span>
              <a 
                href="https://github.com/michaeltheanalyst" 
                target="_blank" 
                rel="noopener noreferrer"
                className="hover:text-primary-600 transition-colors"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

