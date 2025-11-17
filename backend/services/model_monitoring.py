"""
Model performance monitoring and evaluation
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging

from backend.data.data_loader import data_loader
from backend.config import settings
from backend.models.schemas import ModelMetrics

logger = logging.getLogger(__name__)


class ModelMonitoringService:
    """Service for ML model performance monitoring"""
    
    @staticmethod
    def get_model_health() -> Dict[str, Any]:
        """
        Get current model performance metrics
        
        Returns:
            Model health dashboard data
        """
        df = data_loader.get_data()
        
        # Split into recent and previous for comparison
        cutoff = df['timestamp'].max() - timedelta(days=7)
        recent = df[df['timestamp'] >= cutoff]
        previous = df[df['timestamp'] < cutoff]
        
        # Calculate metrics for recent period
        current_metrics = ModelMonitoringService._calculate_metrics(recent)
        previous_metrics = ModelMonitoringService._calculate_metrics(previous)
        
        # Calculate changes
        metrics_change = {
            'precision': round((current_metrics.precision - previous_metrics.precision) * 100, 2),
            'recall': round((current_metrics.recall - previous_metrics.recall) * 100, 2),
            'f1_score': round((current_metrics.f1_score - previous_metrics.f1_score) * 100, 2)
        }
        
        # Simulated inference time (based on complexity)
        avg_inference_time = 0.85  # milliseconds
        
        # Data drift detection
        data_drift_status = ModelMonitoringService._detect_data_drift(recent, previous)
        
        # Feature drift alerts
        feature_drift_alerts = ModelMonitoringService._detect_feature_drift(recent, previous)
        
        # Generate recommendation
        recommendation = ModelMonitoringService._generate_recommendation(
            metrics_change, data_drift_status, feature_drift_alerts
        )
        
        # Simulated last retrain date
        last_retrain = df['timestamp'].max() - timedelta(days=14)
        
        return {
            'current_metrics': current_metrics,
            'metrics_change': metrics_change,
            'avg_inference_time_ms': avg_inference_time,
            'data_drift_status': data_drift_status,
            'feature_drift_alerts': feature_drift_alerts,
            'recommendation': recommendation,
            'last_retrain': last_retrain,
            'model_version': settings.MODEL_VERSION
        }
    
    @staticmethod
    def _calculate_metrics(df: pd.DataFrame) -> ModelMetrics:
        """Calculate classification metrics"""
        
        # Use fraud_probability as predictions (threshold at 0.5)
        y_true = df['is_fraud'].values
        y_pred = (df['fraud_probability'] >= 0.5).values
        
        # Calculate confusion matrix components
        tp = np.sum((y_true == True) & (y_pred == True))
        tn = np.sum((y_true == False) & (y_pred == False))
        fp = np.sum((y_true == False) & (y_pred == True))
        fn = np.sum((y_true == True) & (y_pred == False))
        
        # Calculate metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / len(df) if len(df) > 0 else 0
        
        # Simulated AUC-ROC (would need actual ROC calculation)
        auc_roc = 0.95
        
        return ModelMetrics(
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1_score, 4),
            accuracy=round(accuracy, 4),
            auc_roc=round(auc_roc, 4)
        )
    
    @staticmethod
    def _detect_data_drift(recent: pd.DataFrame, previous: pd.DataFrame) -> str:
        """Detect overall data drift"""
        
        # Compare distributions of key features
        drift_scores = []
        
        for col in ['amount', 'velocity_score', 'spending_deviation_score', 'geo_anomaly_score']:
            # Simple drift detection using mean and std comparison
            recent_mean = recent[col].mean()
            prev_mean = previous[col].mean()
            recent_std = recent[col].std()
            prev_std = previous[col].std()
            
            # Calculate relative change
            mean_change = abs(recent_mean - prev_mean) / (prev_mean + 1e-10)
            std_change = abs(recent_std - prev_std) / (prev_std + 1e-10)
            
            drift_score = (mean_change + std_change) / 2
            drift_scores.append(drift_score)
        
        avg_drift = np.mean(drift_scores)
        
        if avg_drift > 0.15:
            return "HIGH"
        elif avg_drift > 0.08:
            return "MEDIUM"
        else:
            return "LOW"
    
    @staticmethod
    def _detect_feature_drift(recent: pd.DataFrame, previous: pd.DataFrame) -> List[str]:
        """Detect drift in specific features"""
        
        alerts = []
        
        # Check each feature
        for col in ['velocity_score', 'spending_deviation_score', 'geo_anomaly_score', 'amount']:
            recent_mean = recent[col].mean()
            prev_mean = previous[col].mean()
            
            change = abs(recent_mean - prev_mean) / (prev_mean + 1e-10)
            
            if change > 0.12:
                alerts.append(f"{col}: {change*100:.1f}% drift detected")
        
        return alerts
    
    @staticmethod
    def _generate_recommendation(metrics_change: Dict[str, float], 
                                  data_drift: str,
                                  feature_drift: List[str]) -> str:
        """Generate actionable recommendation"""
        
        recommendations = []
        
        # Check metrics degradation
        if metrics_change['recall'] < -2.0:
            recommendations.append("Recall dropped significantly. Retrain with recent data.")
        
        if metrics_change['precision'] < -2.0:
            recommendations.append("Precision decreased. Review false positive patterns.")
        
        # Check drift
        if data_drift == "HIGH":
            recommendations.append("High data drift detected. Immediate retraining recommended.")
        elif data_drift == "MEDIUM":
            recommendations.append("Moderate drift detected. Schedule retraining within 48 hours.")
        
        if len(feature_drift) > 2:
            recommendations.append(f"{len(feature_drift)} features showing drift. Review feature engineering.")
        
        if not recommendations:
            return "Model performing well. Continue monitoring."
        
        return " ".join(recommendations)
    
    @staticmethod
    def get_confusion_matrix() -> Dict[str, Any]:
        """
        Get confusion matrix for model predictions
        
        Returns:
            Confusion matrix data
        """
        df = data_loader.get_data()
        recent = df[df['timestamp'] >= df['timestamp'].max() - timedelta(days=7)]
        
        # Use fraud_probability as predictions
        y_true = recent['is_fraud'].values
        y_pred = (recent['fraud_probability'] >= 0.5).values
        
        # Calculate confusion matrix
        tp = int(np.sum((y_true == True) & (y_pred == True)))
        tn = int(np.sum((y_true == False) & (y_pred == False)))
        fp = int(np.sum((y_true == False) & (y_pred == True)))
        fn = int(np.sum((y_true == True) & (y_pred == False)))
        
        # Calculate rates
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        # Cost impact (simulated)
        # FP cost: $50 per false alarm (customer service)
        # FN cost: Average fraud amount (actual loss)
        fp_cost = fp * 50
        fn_cost = float(recent[(y_true == True) & (y_pred == False)]['amount'].sum())
        total_cost = fp_cost + fn_cost
        
        return {
            'true_positive': tp,
            'true_negative': tn,
            'false_positive': fp,
            'false_negative': fn,
            'false_positive_rate': round(fpr, 4),
            'false_negative_rate': round(fnr, 4),
            'cost_impact': round(total_cost, 2)
        }
    
    @staticmethod
    def get_feature_importance_global() -> List[Dict[str, Any]]:
        """
        Get global feature importance across all predictions
        
        Returns:
            List of features with importance scores
        """
        df = data_loader.get_data()
        
        # Calculate correlation with fraud
        features = ['velocity_score', 'geo_anomaly_score', 'spending_deviation_score', 
                    'time_since_last_transaction', 'amount']
        
        importances = []
        for feature in features:
            # Use correlation as proxy for importance
            corr = df[feature].corr(df['is_fraud'].astype(float))
            importance = abs(corr) * 100
            
            importances.append({
                'feature': feature,
                'importance': round(importance, 2),
                'correlation': round(corr, 3)
            })
        
        # Sort by importance
        importances.sort(key=lambda x: x['importance'], reverse=True)
        
        return importances

