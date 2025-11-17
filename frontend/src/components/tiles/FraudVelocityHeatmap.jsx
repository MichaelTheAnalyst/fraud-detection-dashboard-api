import React from 'react';
import { Activity } from 'lucide-react';
import { Card, CardHeader } from '../shared/Card';
import { useFraudVelocityHeatmap } from '../../hooks/useApi';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

/**
 * Tile 3: Fraud Velocity Heatmap
 * Hourly fraud rate analysis
 */
export const FraudVelocityHeatmap = () => {
  const { data, isLoading, error } = useFraudVelocityHeatmap(24);
  
  if (isLoading) {
    return <Card loading={true} />;
  }
  
  if (error) {
    return (
      <Card className="bg-danger-50">
        <p className="text-danger-700">Failed to load fraud velocity data</p>
      </Card>
    );
  }
  
  // Format data for chart
  const chartData = data?.hourly_rates?.map(rate => ({
    hour: `${rate.hour}:00`,
    rate: rate.fraud_rate,
    isSpike: rate.is_spike,
  })) || [];
  
  return (
    <Card>
      <CardHeader 
        title="Fraud Velocity Heatmap"
        subtitle={`Peak: ${data?.peak_attack_window || 'N/A'}`}
        icon={Activity}
      />
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="hour" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} label={{ value: 'Fraud Rate (%)', angle: -90, position: 'insideLeft' }} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              formatter={(value) => [`${value.toFixed(2)}%`, 'Fraud Rate']}
            />
            <Bar dataKey="rate" radius={[4, 4, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.isSpike ? '#ef4444' : '#0ea5e9'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="text-gray-500">Current Rate:</span>
          <span className="ml-2 font-semibold text-primary-600">
            {data?.current_rate?.toFixed(2) || 0}%
          </span>
        </div>
        <div>
          <span className="text-gray-500">Avg Rate:</span>
          <span className="ml-2 font-semibold text-gray-700">
            {data?.avg_rate?.toFixed(2) || 0}%
          </span>
        </div>
      </div>
    </Card>
  );
};

export default FraudVelocityHeatmap;

