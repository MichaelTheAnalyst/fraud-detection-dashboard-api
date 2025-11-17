/**
 * Utility functions for formatting data
 */

// Format currency
export const formatCurrency = (value) => {
  if (value === null || value === undefined) return '$0.00';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

// Format percentage
export const formatPercentage = (value, decimals = 1) => {
  if (value === null || value === undefined) return '0%';
  return `${value.toFixed(decimals)}%`;
};

// Format large numbers
export const formatNumber = (value) => {
  if (value === null || value === undefined) return '0';
  
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`;
  } else if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`;
  }
  
  return value.toLocaleString();
};

// Format date/time
export const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

// Format date only
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
};

// Format time ago
export const formatTimeAgo = (dateString) => {
  if (!dateString) return 'N/A';
  
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);
  
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };
  
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return `${interval} ${unit}${interval > 1 ? 's' : ''} ago`;
    }
  }
  
  return 'just now';
};

// Get risk level color class
export const getRiskColor = (level) => {
  const colors = {
    critical: 'text-danger-600 bg-danger-50',
    high: 'text-warning-600 bg-warning-50',
    medium: 'text-primary-600 bg-primary-50',
    low: 'text-success-600 bg-success-50',
  };
  return colors[level?.toLowerCase()] || colors.low;
};

// Get risk badge class
export const getRiskBadge = (level) => {
  const badges = {
    critical: 'badge-danger',
    high: 'badge-warning',
    medium: 'badge-info',
    low: 'badge-success',
  };
  return badges[level?.toLowerCase()] || badges.low;
};

// Format confidence score
export const formatConfidence = (value) => {
  if (value === null || value === undefined) return 'N/A';
  const percentage = (value * 100).toFixed(1);
  return `${percentage}%`;
};

// Truncate text
export const truncateText = (text, maxLength = 50) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

// Format account ID (mask middle characters)
export const formatAccountId = (accountId) => {
  if (!accountId) return 'N/A';
  if (accountId.length <= 8) return accountId;
  const start = accountId.substring(0, 4);
  const end = accountId.substring(accountId.length - 4);
  return `${start}****${end}`;
};

