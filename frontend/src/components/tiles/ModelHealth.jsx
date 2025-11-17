import React from 'react';
import { Activity, TrendingDown, TrendingUp } from 'lucide-react';
import { Card, CardHeader } from '../shared/Card';
import { Badge } from '../shared/Badge';
import { useModelHealth } from '../../hooks/useApi';

/**
 * Tile 11: Model Health Dashboard
 * ML model performance monitoring
 */
export const ModelHealth = () => {
  const { data, isLoading, error } = useModelHealth();
  
  if (isLoading) {
    return <Card loading={true} />;
  }
  
  if (error) {
    return (
      <Card className="bg-danger-50">
        <p className="text-danger-700">Failed to load model health data</p>
      </Card>
    );
  }
  
  const metrics = data?.current_metrics || {};
  const changes = data?.metrics_change || {};
  
  const getChangeIcon = (change) => {
    if (change > 0) return <TrendingUp className="h-4 w-4 text-success-600" />;
    if (change < 0) return <TrendingDown className="h-4 w-4 text-danger-600" />;
    return null;
  };
  
  const getStatusBadge = (status) => {
    if (status === 'HIGH') return <Badge variant="danger">High Drift</Badge>;
    if (status === 'MEDIUM') return <Badge variant="warning">Medium Drift</Badge>;
    return <Badge variant="success">Low Drift</Badge>;
  };
  
  return (
    <Card>
      <CardHeader 
        title="Model Health"
        subtitle={`Version: ${data?.model_version || 'N/A'}`}
        icon={Activity}
      />
      
      <div className="space-y-4">
        {/* Performance Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="flex items-center justify-between mb-1">
              <p className="text-sm text-gray-600">Precision</p>
              {getChangeIcon(changes.precision)}
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {(metrics.precision * 100).toFixed(1)}%
            </p>
            {changes.precision !== 0 && (
              <p className={`text-xs mt-1 ${changes.precision > 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {changes.precision > 0 ? '+' : ''}{changes.precision.toFixed(2)}%
              </p>
            )}
          </div>
          
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="flex items-center justify-between mb-1">
              <p className="text-sm text-gray-600">Recall</p>
              {getChangeIcon(changes.recall)}
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {(metrics.recall * 100).toFixed(1)}%
            </p>
            {changes.recall !== 0 && (
              <p className={`text-xs mt-1 ${changes.recall > 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {changes.recall > 0 ? '+' : ''}{changes.recall.toFixed(2)}%
              </p>
            )}
          </div>
          
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-sm text-gray-600 mb-1">F1-Score</p>
            <p className="text-2xl font-bold text-gray-900">
              {(metrics.f1_score * 100).toFixed(1)}%
            </p>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-sm text-gray-600 mb-1">Accuracy</p>
            <p className="text-2xl font-bold text-gray-900">
              {(metrics.accuracy * 100).toFixed(1)}%
            </p>
          </div>
        </div>
        
        {/* System Metrics */}
        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">Inference Time</span>
            <span className="font-semibold text-success-600">
              {data?.avg_inference_time_ms?.toFixed(2) || 0}ms ✓
            </span>
          </div>
          
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">Data Drift</span>
            {getStatusBadge(data?.data_drift_status)}
          </div>
          
          {data?.feature_drift_alerts && data.feature_drift_alerts.length > 0 && (
            <div className="mt-3 p-3 bg-warning-50 border border-warning-200 rounded-lg">
              <p className="text-xs font-semibold text-warning-700 mb-1">Feature Drift Alerts:</p>
              {data.feature_drift_alerts.map((alert, index) => (
                <p key={index} className="text-xs text-warning-600">{alert}</p>
              ))}
            </div>
          )}
        </div>
        
        {/* Recommendation */}
        {data?.recommendation && (
          <div className="bg-primary-50 border border-primary-200 rounded-lg p-3">
            <p className="text-xs font-semibold text-primary-700 mb-1">Recommendation:</p>
            <p className="text-xs text-primary-600">{data.recommendation}</p>
          </div>
        )}
      </div>
    </Card>
  );
};

export default ModelHealth;

