import React from 'react';
import { PieChart } from 'lucide-react';
import { Card, CardHeader } from '../shared/Card';
import { Badge } from '../shared/Badge';
import { useFraudTypeBreakdown } from '../../hooks/useApi';
import { PieChart as RechartsP

ieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

/**
 * Tile 4: Fraud Type Breakdown
 * Distribution of fraud categories
 */
export const FraudTypeBreakdown = () => {
  const { data, isLoading, error } = useFraudTypeBreakdown();
  
  if (isLoading) {
    return <Card loading={true} />;
  }
  
  if (error) {
    return (
      <Card className="bg-danger-50">
        <p className="text-danger-700">Failed to load fraud type data</p>
      </Card>
    );
  }
  
  const COLORS = ['#ef4444', '#f59e0b', '#0ea5e9', '#22c55e', '#8b5cf6'];
  
  const chartData = data?.fraud_types?.map((type, index) => ({
    name: type.fraud_type.replace(/_/g, ' ').toUpperCase(),
    value: type.percentage,
    count: type.count,
    change: type.change_vs_last_week,
  })) || [];
  
  return (
    <Card>
      <CardHeader 
        title="Fraud Type Breakdown"
        subtitle={`Total: ${data?.total_fraud_count?.toLocaleString() || 0}`}
        icon={PieChart}
      />
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RechartsPieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value) => `${value.toFixed(1)}%`}
            />
          </RechartsPieChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mt-4 space-y-2">
        {data?.fraud_types?.slice(0, 3).map((type, index) => (
          <div key={type.fraud_type} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: COLORS[index] }}
              />
              <span className="text-gray-700 capitalize">
                {type.fraud_type.replace(/_/g, ' ')}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-semibold">{type.percentage.toFixed(1)}%</span>
              {type.change_vs_last_week > 20 && (
                <Badge variant="danger">Emerging</Badge>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default FraudTypeBreakdown;

