/**
 * Custom React hooks for API calls using React Query
 */

import { useQuery } from '@tanstack/react-query';
import api from '../services/api';

// Dashboard hooks
export const useExecutiveOverview = (hours = 24) => {
  return useQuery({
    queryKey: ['executive-overview', hours],
    queryFn: async () => {
      const { data } = await api.dashboard.getExecutiveOverview(hours);
      return data;
    },
    refetchInterval: 30000, // Refresh every 30 seconds
  });
};

export const useHighRiskTransactions = (limit = 50) => {
  return useQuery({
    queryKey: ['high-risk-transactions', limit],
    queryFn: async () => {
      const { data } = await api.dashboard.getHighRiskTransactions(limit);
      return data;
    },
    refetchInterval: 10000, // Refresh every 10 seconds
  });
};

export const useFraudVelocityHeatmap = (hours = 24) => {
  return useQuery({
    queryKey: ['fraud-velocity-heatmap', hours],
    queryFn: async () => {
      const { data } = await api.dashboard.getFraudVelocityHeatmap(hours);
      return data;
    },
  });
};

export const useFraudTypeBreakdown = () => {
  return useQuery({
    queryKey: ['fraud-type-breakdown'],
    queryFn: async () => {
      const { data } = await api.dashboard.getFraudTypeBreakdown();
      return data;
    },
  });
};

export const useBehavioralAnomalies = () => {
  return useQuery({
    queryKey: ['behavioral-anomalies'],
    queryFn: async () => {
      const { data } = await api.dashboard.getBehavioralAnomalies();
      return data;
    },
    refetchInterval: 60000, // Refresh every minute
  });
};

export const useSmartAlerts = (hours = 24) => {
  return useQuery({
    queryKey: ['smart-alerts', hours],
    queryFn: async () => {
      const { data } = await api.dashboard.getSmartAlerts(hours);
      return data;
    },
    refetchInterval: 15000, // Refresh every 15 seconds
  });
};

// Analytics hooks
export const useGeoAnomalyHotspots = () => {
  return useQuery({
    queryKey: ['geo-anomaly-hotspots'],
    queryFn: async () => {
      const { data } = await api.analytics.getGeoAnomalyHotspots();
      return data;
    },
  });
};

export const usePredictiveRiskScores = (limit = 127) => {
  return useQuery({
    queryKey: ['predictive-risk-scores', limit],
    queryFn: async () => {
      const { data } = await api.analytics.getPredictiveRiskScores(limit);
      return data;
    },
  });
};

export const useFinancialImpact = (periodDays = 30) => {
  return useQuery({
    queryKey: ['financial-impact', periodDays],
    queryFn: async () => {
      const { data } = await api.analytics.getFinancialImpact(periodDays);
      return data;
    },
  });
};

export const useCustomerExperience = () => {
  return useQuery({
    queryKey: ['customer-experience'],
    queryFn: async () => {
      const { data } = await api.analytics.getCustomerExperience();
      return data;
    },
  });
};

export const useTemporalTrends = (months = 12) => {
  return useQuery({
    queryKey: ['temporal-trends', months],
    queryFn: async () => {
      const { data} = await api.analytics.getTemporalTrends(months);
      return data;
    },
  });
};

export const useMerchantChannelRisk = () => {
  return useQuery({
    queryKey: ['merchant-channel-risk'],
    queryFn: async () => {
      const { data } = await api.analytics.getMerchantChannelRisk();
      return data;
    },
  });
};

// Network hooks
export const useFraudNetworkGraph = (minFraudProb = 0.6) => {
  return useQuery({
    queryKey: ['fraud-network-graph', minFraudProb],
    queryFn: async () => {
      const { data } = await api.network.getFraudNetworkGraph(minFraudProb);
      return data;
    },
  });
};

export const useMuleAccounts = (minSenders = 5) => {
  return useQuery({
    queryKey: ['mule-accounts', minSenders],
    queryFn: async () => {
      const { data } = await api.network.getMuleAccounts(minSenders);
      return data;
    },
  });
};

// Model hooks
export const useModelHealth = () => {
  return useQuery({
    queryKey: ['model-health'],
    queryFn: async () => {
      const { data } = await api.model.getModelHealth();
      return data;
    },
    refetchInterval: 60000, // Refresh every minute
  });
};

export const useConfusionMatrix = () => {
  return useQuery({
    queryKey: ['confusion-matrix'],
    queryFn: async () => {
      const { data } = await api.model.getConfusionMatrix();
      return data;
    },
  });
};

export const useFeatureImportance = () => {
  return useQuery({
    queryKey: ['feature-importance'],
    queryFn: async () => {
      const { data } = await api.model.getFeatureImportance();
      return data;
    },
  });
};

// System hooks
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const { data } = await api.system.getHealth();
      return data;
    },
    refetchInterval: 30000,
  });
};

