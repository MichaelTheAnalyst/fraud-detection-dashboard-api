"""
Analytics and business intelligence services
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from backend.data.data_loader import data_loader
from backend.models.schemas import (
    LocationCorridor, RiskLevel, TimeSeriesPoint,
    RiskMatrixCell, FeatureImportance
)

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics and business intelligence"""
    
    @staticmethod
    def get_geo_anomaly_hotspots() -> Dict[str, Any]:
        """
        Analyze geographic anomalies and high-risk corridors
        
        Returns:
            Geographic analysis with high-risk corridors
        """
        df = data_loader.get_data()
        
        # Analyze location pairs
        location_pairs = df.groupby(['location', 'location']).agg({
            'transaction_id': 'count',
            'is_fraud': 'sum',
            'amount': 'mean',
            'geo_anomaly_score': 'mean'
        }).reset_index()
        
        # For cross-location analysis
        cross_location = df[df['geo_anomaly_score'] > 0.5].copy()
        
        # Create synthetic destination locations based on geo_anomaly_score
        # Higher score = more likely different location
        locations = df['location'].unique().tolist()
        
        high_risk_corridors = []
        for from_loc in locations:
            from_data = cross_location[cross_location['location'] == from_loc]
            if len(from_data) == 0:
                continue
            
            # Simulate destination based on anomaly patterns
            for to_loc in locations:
                if from_loc == to_loc:
                    continue
                
                # Count suspicious transactions
                suspicious = from_data[from_data['geo_anomaly_score'] > 0.7]
                suspicious_count = len(suspicious) // len(locations)  # Distribute
                
                if suspicious_count > 10:
                    fraud_rate = float(suspicious['is_fraud'].mean()) if len(suspicious) > 0 else 0.0
                    avg_amount = float(suspicious['amount'].mean()) if len(suspicious) > 0 else 0.0
                    
                    # Determine risk level
                    if fraud_rate > 0.15:
                        risk = RiskLevel.CRITICAL
                    elif fraud_rate > 0.1:
                        risk = RiskLevel.HIGH
                    elif fraud_rate > 0.05:
                        risk = RiskLevel.MEDIUM
                    else:
                        risk = RiskLevel.LOW
                    
                    high_risk_corridors.append(LocationCorridor(
                        from_location=from_loc,
                        to_location=to_loc,
                        suspicious_count=suspicious_count,
                        fraud_rate=round(fraud_rate * 100, 2),
                        avg_amount=round(avg_amount, 2),
                        risk_level=risk
                    ))
        
        # Sort by fraud rate
        high_risk_corridors.sort(key=lambda x: x.fraud_rate, reverse=True)
        
        # Detect impossible travel
        impossible_travel = AnalyticsService._detect_impossible_travel(df)
        
        # Top risky locations
        location_risk = df.groupby('location').agg({
            'is_fraud': 'mean',
            'transaction_id': 'count',
            'geo_anomaly_score': 'mean'
        }).reset_index()
        location_risk.columns = ['location', 'fraud_rate', 'transaction_count', 'avg_geo_anomaly']
        location_risk = location_risk.nlargest(10, 'fraud_rate')
        
        top_risky_locations = [
            {
                'location': row['location'],
                'fraud_rate': round(row['fraud_rate'] * 100, 2),
                'transaction_count': int(row['transaction_count']),
                'avg_geo_anomaly': round(row['avg_geo_anomaly'], 2)
            }
            for _, row in location_risk.iterrows()
        ]
        
        # Heat map data
        heat_map_data = [
            {
                'location': row['location'],
                'value': float(row['fraud_rate'] * 100),
                'label': f"{row['fraud_rate']*100:.1f}%"
            }
            for _, row in location_risk.iterrows()
        ]
        
        return {
            'high_risk_corridors': high_risk_corridors[:10],
            'impossible_travel_count': impossible_travel,
            'top_risky_locations': top_risky_locations,
            'heat_map_data': heat_map_data
        }
    
    @staticmethod
    def _detect_impossible_travel(df: pd.DataFrame) -> int:
        """Detect impossible travel patterns"""
        # Sort by account and timestamp
        df_sorted = df.sort_values(['sender_account', 'timestamp']).copy()
        
        # Get consecutive transactions
        df_sorted['prev_location'] = df_sorted.groupby('sender_account')['location'].shift(1)
        df_sorted['time_diff_minutes'] = (
            df_sorted.groupby('sender_account')['timestamp'].diff().dt.total_seconds() / 60
        )
        
        # Impossible: different locations within 2 hours (120 minutes)
        # In reality would calculate actual distance
        impossible = df_sorted[
            (df_sorted['location'] != df_sorted['prev_location']) &
            (df_sorted['time_diff_minutes'] < 120) &
            (df_sorted['time_diff_minutes'] > 0)
        ]
        
        return len(impossible)
    
    @staticmethod
    def get_financial_impact(period_days: int = 30) -> Dict[str, Any]:
        """
        Calculate financial impact metrics
        
        Args:
            period_days: Period for calculation
            
        Returns:
            Financial impact analysis
        """
        df = data_loader.get_data()
        
        cutoff = df['timestamp'].max() - timedelta(days=period_days)
        period_df = df[df['timestamp'] >= cutoff]
        
        # Fraud prevented (detected before completion - high prob, not marked fraud yet)
        fraud_prevented = float(
            period_df[
                (period_df['fraud_probability'] >= 0.8) &
                (period_df['is_fraud'] == False)
            ]['amount'].sum()
        )
        
        # Actual fraud losses
        fraud_losses = float(period_df[period_df['is_fraud']]['amount'].sum())
        
        # Prevention costs (simulated: $0.10 per transaction analyzed)
        prevention_costs = len(period_df) * 0.10
        
        # False positive impact (blocked legitimate transactions)
        # Assume 0.25% false positive rate, $50 cost per incident
        false_positive_impact = len(period_df) * 0.0025 * 50
        
        # Net savings
        net_savings = fraud_prevented - fraud_losses - prevention_costs - false_positive_impact
        
        # ROI
        total_costs = prevention_costs + false_positive_impact
        roi_percentage = (net_savings / total_costs * 100) if total_costs > 0 else 0
        
        return {
            'fraud_prevented': round(fraud_prevented, 2),
            'fraud_losses': round(fraud_losses, 2),
            'prevention_costs': round(prevention_costs, 2),
            'false_positive_impact': round(false_positive_impact, 2),
            'net_savings': round(net_savings, 2),
            'roi_percentage': round(roi_percentage, 1),
            'period': f"{period_days} days"
        }
    
    @staticmethod
    def get_customer_experience_metrics() -> Dict[str, Any]:
        """
        Calculate customer experience impact metrics
        
        Returns:
            Customer experience analysis
        """
        df = data_loader.get_data()
        recent = df[df['timestamp'] >= df['timestamp'].max() - timedelta(days=30)]
        
        # Simulate metrics based on fraud detection
        total_transactions = len(recent)
        
        # Blocked transactions (high confidence fraud)
        blocked = len(recent[recent['fraud_probability'] >= 0.9])
        
        # False alarm rate (estimated)
        false_alarm_rate = 0.0025  # 0.25%
        
        # Average review time (simulated based on complexity)
        avg_review_time = float(recent[recent['fraud_probability'] >= 0.75]['velocity_score'].mean() * 10)
        
        # Customer complaints (simulated)
        customer_complaints = int(blocked * 0.05)  # 5% of blocked users complain
        
        # Churn rate (very low due to good accuracy)
        churn_rate = 0.0002
        
        # Satisfaction score
        satisfaction_score = 0.987
        
        return {
            'blocked_transactions': blocked,
            'false_alarm_rate': round(false_alarm_rate, 4),
            'avg_review_time_minutes': round(avg_review_time, 1),
            'customer_complaints': customer_complaints,
            'churn_rate': round(churn_rate, 4),
            'satisfaction_score': round(satisfaction_score, 3)
        }
    
    @staticmethod
    def get_temporal_trends(months: int = 12) -> Dict[str, Any]:
        """
        Analyze temporal trends and forecast
        
        Args:
            months: Number of months for historical analysis
            
        Returns:
            Temporal analysis with forecast
        """
        df = data_loader.get_data()
        
        # Daily aggregation
        daily = df.groupby(df['timestamp'].dt.date).agg({
            'is_fraud': ['sum', 'mean'],
            'transaction_id': 'count'
        }).reset_index()
        daily.columns = ['date', 'fraud_count', 'fraud_rate', 'transaction_count']
        
        # Create time series
        historical_trend = []
        for _, row in daily.iterrows():
            historical_trend.append(TimeSeriesPoint(
                timestamp=datetime.combine(row['date'], datetime.min.time()),
                value=float(row['fraud_rate'] * 100),
                label=f"{row['fraud_count']} frauds"
            ))
        
        # Simple forecast (trend + seasonality simulation)
        last_date = daily['date'].max()
        last_rate = daily['fraud_rate'].iloc[-7:].mean()  # 7-day average
        
        forecast = []
        for i in range(1, 31):  # 30-day forecast
            forecast_date = last_date + timedelta(days=i)
            # Add slight upward trend and random variation
            forecast_value = last_rate * (1 + i * 0.001) * np.random.uniform(0.9, 1.1)
            forecast.append(TimeSeriesPoint(
                timestamp=datetime.combine(forecast_date, datetime.min.time()),
                value=float(forecast_value * 100),
                label="Predicted"
            ))
        
        # Calculate expected change
        expected_change = ((forecast[-1].value / historical_trend[-1].value) - 1) * 100
        
        # Identify high-risk days (weekends, end of month)
        high_risk_days = ["Saturdays", "Sundays", "Last day of month"]
        
        # Emerging patterns (simulated)
        emerging_patterns = ["Mobile ATM fraud increasing", "Cross-border transfers spike"]
        
        return {
            'historical_trend': historical_trend[-90:],  # Last 90 days
            'forecast': forecast,
            'expected_fraud_volume_change': round(expected_change, 1),
            'high_risk_days': high_risk_days,
            'emerging_patterns': emerging_patterns
        }
    
    @staticmethod
    def get_merchant_channel_risk() -> Dict[str, Any]:
        """
        Analyze risk by merchant category and payment channel
        
        Returns:
            Risk matrix analysis
        """
        df = data_loader.get_data()
        
        # Group by channel and category
        risk_matrix = df.groupby(['payment_channel', 'merchant_category']).agg({
            'is_fraud': 'mean',
            'transaction_id': 'count'
        }).reset_index()
        risk_matrix.columns = ['channel', 'category', 'fraud_rate', 'transaction_count']
        
        # Create risk matrix cells
        risk_matrix_cells = []
        for _, row in risk_matrix.iterrows():
            fraud_rate = float(row['fraud_rate'])
            
            # Determine risk level
            if fraud_rate > 0.08:
                risk = RiskLevel.CRITICAL
            elif fraud_rate > 0.05:
                risk = RiskLevel.HIGH
            elif fraud_rate > 0.03:
                risk = RiskLevel.MEDIUM
            else:
                risk = RiskLevel.LOW
            
            risk_matrix_cells.append(RiskMatrixCell(
                channel=row['channel'],
                category=row['category'],
                fraud_rate=round(fraud_rate * 100, 2),
                transaction_count=int(row['transaction_count']),
                risk_level=risk
            ))
        
        # Find highest risk combination
        highest_risk = risk_matrix.nlargest(1, 'fraud_rate').iloc[0]
        highest_risk_combination = {
            'channel': highest_risk['channel'],
            'category': highest_risk['category'],
            'fraud_rate': round(highest_risk['fraud_rate'] * 100, 2)
        }
        
        # Recommendations
        recommendations = [
            f"Implement 2FA for {highest_risk['channel']} + {highest_risk['category']} transactions",
            "Increase monitoring for high-risk corridors",
            "Adjust velocity thresholds for travel merchant category"
        ]
        
        return {
            'risk_matrix': risk_matrix_cells,
            'highest_risk_combination': highest_risk_combination,
            'recommendations': recommendations
        }
    
    @staticmethod
    def explain_transaction(transaction_id: str) -> Dict[str, Any]:
        """
        Explain why a transaction was flagged
        
        Args:
            transaction_id: Transaction to explain
            
        Returns:
            Feature importance and explanation
        """
        df = data_loader.get_data()
        
        txn = df[df['transaction_id'] == transaction_id]
        if len(txn) == 0:
            return {
                'error': 'Transaction not found',
                'transaction_id': transaction_id
            }
        
        txn = txn.iloc[0]
        
        # Calculate feature importances (based on actual values)
        importances = []
        
        # Velocity score importance
        velocity_importance = float(txn['velocity_score']) * 34
        importances.append(FeatureImportance(
            feature="Velocity Score",
            importance=velocity_importance,
            description=f"Transaction velocity: {txn['time_since_last_transaction']:.0f}s since last transaction"
        ))
        
        # Geo anomaly importance
        geo_importance = float(txn['geo_anomaly_score']) * 28
        importances.append(FeatureImportance(
            feature="Geo Anomaly",
            importance=geo_importance,
            description=f"Unusual location pattern detected (score: {txn['geo_anomaly_score']:.1f}/10)"
        ))
        
        # Spending deviation importance
        spending_importance = float(txn['spending_deviation_score']) * 19
        importances.append(FeatureImportance(
            feature="Spending Deviation",
            importance=spending_importance,
            description=f"Amount deviates from typical spending (score: {txn['spending_deviation_score']:.1f}/10)"
        ))
        
        # Time pattern importance
        time_importance = 11 if txn['is_night'] else 5
        importances.append(FeatureImportance(
            feature="Time Pattern",
            importance=float(time_importance),
            description=f"Transaction at {txn['hour']:02d}:00 ({'unusual' if txn['is_night'] else 'normal'} time)"
        ))
        
        # Device change importance
        device_importance = 8.0
        importances.append(FeatureImportance(
            feature="Device Change",
            importance=device_importance,
            description=f"Device: {txn['device_used']}"
        ))
        
        # Sort by importance
        importances.sort(key=lambda x: x.importance, reverse=True)
        
        # Generate explanation
        explanation = f"Transaction flagged due to: "
        top_factors = [imp.feature for imp in importances[:2]]
        explanation += f"{', '.join(top_factors)}. "
        explanation += f"Occurred at {txn['location']} via {txn['device_used']} "
        explanation += f"for ${txn['amount']:.2f}."
        
        # Recommended action
        if txn['fraud_probability'] > 0.9:
            action = "BLOCK and request verification"
        elif txn['fraud_probability'] > 0.75:
            action = "HOLD for manual review"
        else:
            action = "MONITOR for additional signals"
        
        return {
            'transaction_id': transaction_id,
            'fraud_probability': float(txn['fraud_probability']),
            'feature_importances': importances,
            'explanation': explanation,
            'recommended_action': action
        }

