import React from 'react';
import clsx from 'clsx';
import { getRiskBadge } from '../../utils/formatters';

export const Badge = ({ children, variant = 'default', className }) => {
  const variants = {
    default: 'badge-info',
    success: 'badge-success',
    warning: 'badge-warning',
    danger: 'badge-danger',
  };
  
  return (
    <span className={clsx('badge', variants[variant], className)}>
      {children}
    </span>
  );
};

export const RiskBadge = ({ level }) => {
  const badgeClass = getRiskBadge(level);
  
  return (
    <span className={clsx('badge', badgeClass)}>
      {level?.toUpperCase() || 'UNKNOWN'}
    </span>
  );
};

export default Badge;

