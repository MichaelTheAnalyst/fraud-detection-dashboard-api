import React from 'react';
import { AlertTriangle, Eye } from 'lucide-react';
import { Card, CardHeader } from '../shared/Card';
import { RiskBadge } from '../shared/Badge';
import { useHighRiskTransactions } from '../../hooks/useApi';
import { formatCurrency, formatDateTime, formatConfidence } from '../../utils/formatters';

/**
 * Tile 2: High-Risk Transactions Feed
 * Critical alerts requiring immediate attention
 */
export const HighRiskTransactions = () => {
  const { data, isLoading, error } = useHighRiskTransactions(20);
  
  if (isLoading) {
    return (
      <Card loading={true} />
    );
  }
  
  if (error) {
    return (
      <Card className="bg-danger-50">
        <p className="text-danger-700">Failed to load high-risk transactions</p>
      </Card>
    );
  }
  
  const criticalAlerts = data?.critical_alerts || [];
  
  return (
    <Card>
      <CardHeader 
        title="High-Risk Transactions"
        subtitle={`${data?.total_alerts || 0} total alerts`}
        icon={AlertTriangle}
      />
      
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {criticalAlerts.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No high-risk transactions</p>
        ) : (
          criticalAlerts.map((transaction) => (
            <div 
              key={transaction.transaction_id}
              className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-sm font-medium">
                      {transaction.transaction_id}
                    </span>
                    <RiskBadge level={transaction.risk_level} />
                  </div>
                  <p className="text-xs text-gray-600">
                    {transaction.fraud_type || 'Unknown Type'}
                  </p>
                </div>
                <span className="text-lg font-bold text-gray-900">
                  {formatCurrency(transaction.amount)}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                <div>
                  <span className="text-gray-500">Location:</span> {transaction.location}
                </div>
                <div>
                  <span className="text-gray-500">Device:</span> {transaction.device_used}
                </div>
                <div>
                  <span className="text-gray-500">Confidence:</span> {formatConfidence(transaction.confidence)}
                </div>
                <div>
                  <span className="text-gray-500">Time:</span> {formatDateTime(transaction.timestamp)}
                </div>
              </div>
              
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-gray-500">
                  {transaction.time_since_last?.toFixed(0) || 0}s since last transaction
                </span>
                <button className="text-xs text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1">
                  <Eye className="h-3 w-3" />
                  Investigate
                </button>
              </div>
            </div>
          ))
        )}
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-gray-500">High Priority:</span>
          <span className="ml-2 font-semibold text-warning-600">
            {data?.high_priority_count || 0}
          </span>
        </div>
        <div>
          <span className="text-gray-500">Medium Priority:</span>
          <span className="ml-2 font-semibold text-primary-600">
            {data?.medium_priority_count || 0}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default HighRiskTransactions;

