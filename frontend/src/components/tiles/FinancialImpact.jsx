import React from 'react';
import { DollarSign, TrendingUp } from 'lucide-react';
import { Card, CardHeader } from '../shared/Card';
import { useFinancialImpact } from '../../hooks/useApi';
import { formatCurrency, formatNumber } from '../../utils/formatters';

/**
 * Tile 14: Financial Impact Scorecard
 * ROI and cost analysis
 */
export const FinancialImpact = () => {
  const { data, isLoading, error } = useFinancialImpact(30);
  
  if (isLoading) {
    return <Card loading={true} />;
  }
  
  if (error) {
    return (
      <Card className="bg-danger-50">
        <p className="text-danger-700">Failed to load financial impact data</p>
      </Card>
    );
  }
  
  return (
    <Card>
      <CardHeader 
        title="Financial Impact"
        subtitle={`Last ${data?.period || '30 days'}`}
        icon={DollarSign}
      />
      
      <div className="space-y-4">
        {/* Net Savings - Hero Metric */}
        <div className="bg-success-50 rounded-lg p-4 border border-success-200">
          <p className="text-sm text-success-700 mb-1">Net Savings</p>
          <p className="text-3xl font-bold text-success-900">
            {formatCurrency(data?.net_savings)}
          </p>
          <div className="flex items-center gap-2 mt-2">
            <TrendingUp className="h-4 w-4 text-success-600" />
            <span className="text-sm font-semibold text-success-700">
              ROI: {formatNumber(data?.roi_percentage)}%
            </span>
          </div>
        </div>
        
        {/* Breakdown */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Fraud Prevented</span>
            <span className="text-lg font-semibold text-success-600">
              {formatCurrency(data?.fraud_prevented)}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Fraud Losses</span>
            <span className="text-lg font-semibold text-danger-600">
              -{formatCurrency(data?.fraud_losses)}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Prevention Costs</span>
            <span className="text-lg font-semibold text-gray-700">
              -{formatCurrency(data?.prevention_costs)}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">False Positive Impact</span>
            <span className="text-lg font-semibold text-gray-700">
              -{formatCurrency(data?.false_positive_impact)}
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default FinancialImpact;

