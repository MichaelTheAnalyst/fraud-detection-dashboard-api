import React from 'react';
import { AlertTriangle, DollarSign, Clock, Bell, TrendingUp } from 'lucide-react';
import { StatCard } from '../shared/Card';
import { useExecutiveOverview } from '../../hooks/useApi';
import { formatCurrency, formatPercentage, formatNumber } from '../../utils/formatters';

/**
 * Tile 1: Executive Overview
 * Real-time fraud pulse with key KPIs
 */
export const ExecutiveOverview = () => {
  const { data, isLoading, error } = useExecutiveOverview(24);
  
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="stat-card animate-pulse">
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="card bg-danger-50 border-danger-200">
        <p className="text-danger-700">Failed to load executive overview</p>
      </div>
    );
  }
  
  const stats = [
    {
      title: 'Fraud Amount Today',
      value: formatCurrency(data?.fraud_amount_today),
      icon: DollarSign,
      trend: data?.fraud_rate_change > 0 ? 'up' : 'down',
      change: data?.fraud_rate_change ? `${data.fraud_rate_change > 0 ? '+' : ''}${data.fraud_rate_change.toFixed(1)}%` : null,
    },
    {
      title: 'Fraud Rate (24H)',
      value: formatPercentage(data?.fraud_rate_24h),
      icon: TrendingUp,
      trend: data?.fraud_rate_change > 0 ? 'up' : 'down',
      change: data?.fraud_rate_change ? `${data.fraud_rate_change > 0 ? '+' : ''}${data.fraud_rate_change.toFixed(1)}%` : null,
    },
    {
      title: 'Blocked Amount',
      value: formatCurrency(data?.blocked_amount),
      icon: AlertTriangle,
    },
    {
      title: 'Avg Detection Time',
      value: `${data?.avg_detection_time?.toFixed(2) || 0}s`,
      icon: Clock,
    },
    {
      title: 'Alerts Pending',
      value: formatNumber(data?.alerts_pending),
      icon: Bell,
    },
  ];
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 fade-in">
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
};

export default ExecutiveOverview;

