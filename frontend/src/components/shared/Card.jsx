import React from 'react';
import { Loader2 } from 'lucide-react';
import clsx from 'clsx';

export const Card = ({ children, className, loading = false }) => {
  return (
    <div className={clsx('card', className)}>
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
        </div>
      ) : (
        children
      )}
    </div>
  );
};

export const CardHeader = ({ title, subtitle, action, icon: Icon }) => {
  return (
    <div className="card-header">
      <div className="flex items-center gap-2">
        {Icon && <Icon className="h-5 w-5 text-gray-600" />}
        <div>
          <h3 className="card-title">{title}</h3>
          {subtitle && <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>}
        </div>
      </div>
      {action && <div>{action}</div>}
    </div>
  );
};

export const StatCard = ({ title, value, change, icon: Icon, trend }) => {
  const isPositive = trend === 'up';
  const isNegative = trend === 'down';
  
  return (
    <div className="stat-card">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {change !== undefined && (
            <p className={clsx(
              'text-sm mt-1 font-medium',
              isPositive && 'text-success-600',
              isNegative && 'text-danger-600',
              !isPositive && !isNegative && 'text-gray-600'
            )}>
              {change > 0 ? '+' : ''}{change}
            </p>
          )}
        </div>
        {Icon && (
          <div className="bg-primary-50 p-3 rounded-lg">
            <Icon className="h-6 w-6 text-primary-600" />
          </div>
        )}
      </div>
    </div>
  );
};

export default Card;

