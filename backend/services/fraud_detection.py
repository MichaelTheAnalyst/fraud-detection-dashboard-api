"""
Core fraud detection business logic
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from backend.data.data_loader import data_loader
from backend.models.schemas import (
    HighRiskTransaction, RiskLevel, FraudTypeStats,
    AccountAtRisk, BehavioralAnomaly, Alert
)

logger = logging.getLogger(__name__)


class FraudDetectionService:
    """Service for fraud detection operations"""
    
    @staticmethod
    def get_executive_overview(hours: int = 24) -> Dict[str, Any]:
        """
        Calculate executive overview metrics
        
        Args:
            hours: Time window in hours
            
        Returns:
            Dictionary with KPI metrics
        """
        df = data_loader.get_data()
        
        # Current period
        cutoff = df['timestamp'].max() - timedelta(hours=hours)
        current = df[df['timestamp'] >= cutoff]
        
        # Previous period for comparison
        prev_cutoff = cutoff - timedelta(hours=hours)
        previous = df[(df['timestamp'] >= prev_cutoff) & (df['timestamp'] < cutoff)]
        
        # Calculate metrics
        fraud_amount_today = float(current[current['is_fraud']]['amount'].sum())
        fraud_rate_24h = float(current['is_fraud'].mean() * 100)
        prev_fraud_rate = float(previous['is_fraud'].mean() * 100) if len(previous) > 0 else fraud_rate_24h
        fraud_rate_change = fraud_rate_24h - prev_fraud_rate
        
        # Simulate blocked amount (amount that would have been lost)
        blocked_amount = float(current[current['fraud_probability'] >= 0.75]['amount'].sum())
        
        # Simulate detection time (based on velocity score - higher = faster detection)
        avg_detection_time = float(current['velocity_score'].mean() * 2)  # Scaled to seconds
        
        # Count alerts
        alerts_pending = int(len(current[current['fraud_probability'] >= 0.75]))
        
        return {
            'fraud_amount_today': round(fraud_amount_today, 2),
            'fraud_rate_24h': round(fraud_rate_24h, 2),
            'fraud_rate_change': round(fraud_rate_change, 2),
            'blocked_amount': round(blocked_amount, 2),
            'avg_detection_time': round(avg_detection_time, 2),
            'alerts_pending': alerts_pending,
            'timestamp': datetime.now()
        }
    
    @staticmethod
    def get_high_risk_transactions(limit: int = 50) -> Dict[str, Any]:
        """
        Get high-risk transactions feed
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            Dictionary with categorized high-risk transactions
        """
        df = data_loader.get_data()
        
        # Get recent high-risk transactions
        recent_cutoff = df['timestamp'].max() - timedelta(hours=24)
        recent = df[df['timestamp'] >= recent_cutoff].copy()
        
        # Sort by fraud probability
        high_risk = recent[recent['fraud_probability'] >= 0.75].nlargest(limit, 'fraud_probability')
        
        critical_alerts = []
        for _, row in high_risk.iterrows():
            # Handle NA/null values
            fraud_type = row.get('fraud_type')
            if pd.isna(fraud_type):
                fraud_type = 'Unknown'
            
            critical_alerts.append(HighRiskTransaction(
                transaction_id=str(row['transaction_id']),
                amount=float(row['amount']),
                fraud_type=str(fraud_type),
                location=str(row['location']),
                device_used=str(row['device_used']),
                confidence=float(row['fraud_probability']),
                time_since_last=float(row['time_since_last_transaction']),
                timestamp=row['timestamp'],
                risk_level=RiskLevel.CRITICAL if row['fraud_probability'] >= 0.9 else RiskLevel.HIGH,
                sender_account=str(row['sender_account']),
                receiver_account=str(row['receiver_account'])
            ))
        
        # Count by priority
        high_priority_count = int(len(recent[recent['fraud_probability'].between(0.6, 0.75)]))
        medium_priority_count = int(len(recent[recent['fraud_probability'].between(0.4, 0.6)]))
        
        return {
            'critical_alerts': critical_alerts[:20],  # Top 20
            'high_priority_count': high_priority_count,
            'medium_priority_count': medium_priority_count,
            'total_alerts': len(critical_alerts) + high_priority_count + medium_priority_count,
            'last_updated': datetime.now()
        }
    
    @staticmethod
    def get_fraud_velocity_heatmap(hours: int = 24) -> Dict[str, Any]:
        """
        Calculate fraud velocity by hour
        
        Args:
            hours: Time window
            
        Returns:
            Hourly fraud rate analysis
        """
        df = data_loader.get_data()
        
        cutoff = df['timestamp'].max() - timedelta(hours=hours)
        recent = df[df['timestamp'] >= cutoff].copy()
        
        # Group by hour
        hourly = recent.groupby('hour').agg({
            'is_fraud': ['sum', 'count', 'mean']
        }).reset_index()
        
        hourly.columns = ['hour', 'fraud_count', 'transaction_count', 'fraud_rate']
        
        # Detect spikes (rate > 1.5x average)
        avg_rate = hourly['fraud_rate'].mean()
        spike_threshold = avg_rate * 1.5
        
        hourly_rates = []
        for _, row in hourly.iterrows():
            hourly_rates.append({
                'hour': int(row['hour']),
                'fraud_rate': float(row['fraud_rate'] * 100),
                'transaction_count': int(row['transaction_count']),
                'fraud_count': int(row['fraud_count']),
                'is_spike': bool(row['fraud_rate'] > spike_threshold)
            })
        
        # Find peak attack window
        peak_hour = hourly.loc[hourly['fraud_rate'].idxmax(), 'hour']
        peak_attack_window = f"{int(peak_hour):02d}:00-{int(peak_hour)+1:02d}:00"
        
        return {
            'hourly_rates': hourly_rates,
            'peak_attack_window': peak_attack_window,
            'current_rate': float(hourly['fraud_rate'].iloc[-1] * 100) if len(hourly) > 0 else 0.0,
            'avg_rate': float(avg_rate * 100)
        }
    
    @staticmethod
    def get_fraud_type_breakdown() -> Dict[str, Any]:
        """
        Analyze fraud by type
        
        Returns:
            Fraud type statistics
        """
        df = data_loader.get_data()
        fraud_df = df[df['is_fraud'] == True].copy()
        
        # Current week
        week_cutoff = df['timestamp'].max() - timedelta(days=7)
        current_week = fraud_df[fraud_df['timestamp'] >= week_cutoff]
        
        # Previous week
        prev_week_cutoff = week_cutoff - timedelta(days=7)
        previous_week = fraud_df[
            (fraud_df['timestamp'] >= prev_week_cutoff) & 
            (fraud_df['timestamp'] < week_cutoff)
        ]
        
        # Calculate stats by type
        fraud_types = []
        current_counts = current_week['fraud_type'].value_counts()
        prev_counts = previous_week['fraud_type'].value_counts()
        total_fraud = len(fraud_df)
        
        for fraud_type, count in fraud_df['fraud_type'].value_counts().items():
            if pd.isna(fraud_type):
                continue
                
            percentage = (count / total_fraud) * 100
            
            # Calculate change
            current_type_count = current_counts.get(fraud_type, 0)
            prev_type_count = prev_counts.get(fraud_type, 0)
            change = 0.0
            if prev_type_count > 0:
                change = ((current_type_count - prev_type_count) / prev_type_count) * 100
            
            avg_amount = float(fraud_df[fraud_df['fraud_type'] == fraud_type]['amount'].mean())
            
            fraud_types.append(FraudTypeStats(
                fraud_type=fraud_type,
                percentage=round(percentage, 1),
                count=int(count),
                change_vs_last_week=round(change, 1),
                avg_amount=round(avg_amount, 2)
            ))
        
        # Sort by percentage
        fraud_types.sort(key=lambda x: x.percentage, reverse=True)
        
        # Find emerging threats (>20% increase)
        emerging = [ft.fraud_type for ft in fraud_types if ft.change_vs_last_week > 20]
        
        return {
            'fraud_types': fraud_types,
            'total_fraud_count': int(len(fraud_df)),
            'dominant_type': fraud_types[0].fraud_type if fraud_types else 'Unknown',
            'emerging_threats': emerging
        }
    
    @staticmethod
    def get_predictive_risk_scores(limit: int = 127) -> Dict[str, Any]:
        """
        Predict accounts at risk in next 24 hours
        
        Args:
            limit: Maximum accounts to return
            
        Returns:
            Accounts predicted to be at risk
        """
        df = data_loader.get_data()
        
        # Get recent non-fraud transactions with high risk indicators
        recent = df[df['timestamp'] >= df['timestamp'].max() - timedelta(days=7)].copy()
        
        # Calculate risk score per account
        account_risk = recent.groupby('sender_account').agg({
            'velocity_score': 'mean',
            'spending_deviation_score': 'mean',
            'geo_anomaly_score': 'mean',
            'fraud_probability': 'max',
            'timestamp': 'max',
            'device_used': 'nunique',
            'location': 'nunique'
        }).reset_index()
        
        # Calculate composite risk
        account_risk['risk_score'] = (
            account_risk['fraud_probability'] * 0.5 +
            account_risk['velocity_score'] * 0.2 +
            account_risk['geo_anomaly_score'] * 0.15 +
            account_risk['spending_deviation_score'] * 0.15
        )
        
        # Get top at-risk accounts
        at_risk = account_risk.nlargest(limit, 'risk_score')
        
        high_probability_targets = []
        for _, row in at_risk.head(20).iterrows():
            risk_factors = []
            if row['velocity_score'] > 0.7:
                risk_factors.append("Unusual velocity spike")
            if row['device_used'] > 2:
                risk_factors.append("New device detected")
            if row['geo_anomaly_score'] > 0.7:
                risk_factors.append(f"Geo-anomaly score: {row['geo_anomaly_score']:.1f}/10")
            if row['spending_deviation_score'] > 0.7:
                risk_factors.append(f"Spending deviation: +{row['spending_deviation_score']*100:.0f}%")
            
            high_probability_targets.append(AccountAtRisk(
                account_id=row['sender_account'],
                fraud_risk=float(row['risk_score']),
                risk_factors=risk_factors,
                recent_anomalies=[f"Location changes: {int(row['location'])}"],
                recommended_action="Enable 2FA" if row['risk_score'] > 0.8 else "Monitor closely",
                last_transaction_time=row['timestamp']
            ))
        
        # Risk distribution
        risk_distribution = {
            'critical': int(len(at_risk[at_risk['risk_score'] >= 0.85])),
            'high': int(len(at_risk[at_risk['risk_score'].between(0.7, 0.85)])),
            'medium': int(len(at_risk[at_risk['risk_score'].between(0.5, 0.7)])),
            'low': int(len(at_risk[at_risk['risk_score'] < 0.5]))
        }
        
        return {
            'high_probability_targets': high_probability_targets,
            'total_at_risk': len(at_risk),
            'risk_distribution': risk_distribution,
            'prediction_confidence': 0.87
        }
    
    @staticmethod
    def get_behavioral_anomalies() -> Dict[str, Any]:
        """
        Detect behavioral anomalies
        
        Returns:
            List of detected anomalies
        """
        df = data_loader.get_data()
        recent = df[df['timestamp'] >= df['timestamp'].max() - timedelta(days=7)].copy()
        
        anomalies = []
        
        # Testing phase detection (small then large)
        testing_accounts = FraudDetectionService._detect_testing_phase(recent)
        if testing_accounts > 0:
            anomalies.append(BehavioralAnomaly(
                anomaly_type="testing_phase",
                affected_accounts=testing_accounts,
                description="Small transactions followed by large transactions pattern",
                severity=RiskLevel.HIGH
            ))
        
        # Device switching
        device_switching = len(recent.groupby('sender_account')['device_used'].nunique()[
            recent.groupby('sender_account')['device_used'].nunique() > 2
        ])
        if device_switching > 0:
            anomalies.append(BehavioralAnomaly(
                anomaly_type="device_switching",
                affected_accounts=device_switching,
                description="Multiple devices used in short time window",
                severity=RiskLevel.MEDIUM
            ))
        
        # Dormant account reactivation
        dormant_reactivation = FraudDetectionService._detect_dormant_reactivation(df)
        if dormant_reactivation > 0:
            anomalies.append(BehavioralAnomaly(
                anomaly_type="dormant_reactivation",
                affected_accounts=dormant_reactivation,
                description="Inactive accounts (90+ days) suddenly active",
                severity=RiskLevel.CRITICAL
            ))
        
        return {
            'anomalies': anomalies,
            'total_anomalies': len(anomalies),
            'last_updated': datetime.now()
        }
    
    @staticmethod
    def _detect_testing_phase(df: pd.DataFrame) -> int:
        """Detect accounts with testing phase pattern"""
        # Group by account and check for small-then-large pattern
        account_patterns = df.groupby('sender_account')['amount'].apply(list)
        testing_count = 0
        
        for amounts in account_patterns:
            if len(amounts) >= 3:
                # Check if first transactions are small (<50) and later ones large (>500)
                early = amounts[:2]
                late = amounts[-2:]
                if all(a < 50 for a in early) and any(a > 500 for a in late):
                    testing_count += 1
        
        return testing_count
    
    @staticmethod
    def _detect_dormant_reactivation(df: pd.DataFrame) -> int:
        """Detect dormant accounts that suddenly reactivate"""
        # Calculate time gaps between transactions per account
        df_sorted = df.sort_values(['sender_account', 'timestamp'])
        df_sorted['time_gap'] = df_sorted.groupby('sender_account')['timestamp'].diff().dt.days
        
        # Find accounts with 90+ day gap followed by activity
        dormant_accounts = df_sorted[df_sorted['time_gap'] >= 90]['sender_account'].unique()
        
        return len(dormant_accounts)
    
    @staticmethod
    def generate_smart_alerts(hours: int = 24) -> Dict[str, Any]:
        """
        Generate smart alerts based on various conditions
        
        Args:
            hours: Time window
            
        Returns:
            Categorized alerts
        """
        df = data_loader.get_data()
        cutoff = df['timestamp'].max() - timedelta(hours=hours)
        recent = df[df['timestamp'] >= cutoff]
        
        critical_alerts = []
        warning_alerts = []
        info_alerts = []
        
        # Check for fraud rate spike
        current_rate = recent['is_fraud'].mean()
        overall_rate = df['is_fraud'].mean()
        
        if current_rate > overall_rate * 2:
            critical_alerts.append(Alert(
                alert_id=f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_001",
                severity=RiskLevel.CRITICAL,
                title="Fraud Rate Spike Detected",
                description=f"Fraud rate increased to {current_rate*100:.1f}% (+{(current_rate-overall_rate)*100:.1f}%)",
                timestamp=datetime.now()
            ))
        
        # Check for network anomalies
        fraud_rings = FraudDetectionService._detect_simple_rings(recent)
        if fraud_rings > 0:
            critical_alerts.append(Alert(
                alert_id=f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_002",
                severity=RiskLevel.CRITICAL,
                title=f"{fraud_rings} Fraud Ring(s) Detected",
                description=f"Circular transaction patterns detected involving multiple accounts",
                timestamp=datetime.now()
            ))
        
        # Model performance warning (simulated)
        if np.random.random() < 0.3:  # 30% chance for demo
            warning_alerts.append(Alert(
                alert_id=f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_003",
                severity=RiskLevel.MEDIUM,
                title="Model Performance Degradation",
                description="Recall dropped 2.3% in the last week. Retrain recommended.",
                timestamp=datetime.now()
            ))
        
        # Info: High volume period
        if len(recent) > df.groupby(df['timestamp'].dt.date).size().mean() * 1.2:
            info_alerts.append(Alert(
                alert_id=f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}_004",
                severity=RiskLevel.LOW,
                title="High Transaction Volume",
                description=f"Transaction volume 20% above average: {len(recent):,} transactions",
                timestamp=datetime.now()
            ))
        
        return {
            'critical_alerts': critical_alerts,
            'warning_alerts': warning_alerts,
            'info_alerts': info_alerts,
            'total_unread': len(critical_alerts) + len(warning_alerts) + len(info_alerts),
            'last_updated': datetime.now()
        }
    
    @staticmethod
    def _detect_simple_rings(df: pd.DataFrame) -> int:
        """Simple fraud ring detection"""
        # Look for circular patterns: A->B, B->C, C->A
        transactions = df[['sender_account', 'receiver_account', 'fraud_probability']]
        high_risk = transactions[transactions['fraud_probability'] > 0.7]
        
        # Create adjacency list
        graph = defaultdict(set)
        for _, row in high_risk.iterrows():
            graph[row['sender_account']].add(row['receiver_account'])
        
        # Simple cycle detection
        rings = 0
        visited = set()
        
        for node in graph:
            if node in visited:
                continue
            # Check if any neighbor points back to this node (simple 2-cycle)
            for neighbor in graph[node]:
                if node in graph.get(neighbor, set()):
                    rings += 1
                    visited.add(node)
                    visited.add(neighbor)
                    break
        
        return rings

