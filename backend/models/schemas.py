"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FraudType(str, Enum):
    """Types of fraud"""
    ACCOUNT_TAKEOVER = "account_takeover"
    MONEY_LAUNDERING = "money_laundering"
    CARD_FRAUD = "card_fraud"
    IDENTITY_THEFT = "identity_theft"
    SYNTHETIC_ID = "synthetic_id"


class TransactionType(str, Enum):
    """Transaction types"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"


# Response Models

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    data_loaded: bool
    data_info: Optional[Dict[str, Any]] = None


class ExecutiveOverviewResponse(BaseModel):
    """Tier 1: Executive Overview metrics"""
    fraud_amount_today: float = Field(..., description="Total fraud amount in last 24h")
    fraud_rate_24h: float = Field(..., description="Fraud rate percentage")
    fraud_rate_change: float = Field(..., description="Change from previous period")
    blocked_amount: float = Field(..., description="Amount of fraud blocked/prevented")
    avg_detection_time: float = Field(..., description="Average detection time in seconds")
    alerts_pending: int = Field(..., description="Number of pending alerts")
    timestamp: datetime


class HighRiskTransaction(BaseModel):
    """High-risk transaction details"""
    transaction_id: str
    amount: float
    fraud_type: Optional[str]
    location: str
    device_used: str
    confidence: float = Field(..., description="Fraud probability 0-1")
    time_since_last: float = Field(..., description="Seconds since last transaction")
    timestamp: datetime
    risk_level: RiskLevel
    sender_account: str
    receiver_account: str


class HighRiskTransactionsFeedResponse(BaseModel):
    """Tile 1: High-risk transactions feed"""
    critical_alerts: List[HighRiskTransaction]
    high_priority_count: int
    medium_priority_count: int
    total_alerts: int
    last_updated: datetime


class HourlyFraudRate(BaseModel):
    """Fraud rate for specific hour"""
    hour: int
    fraud_rate: float
    transaction_count: int
    fraud_count: int
    is_spike: bool


class FraudVelocityHeatmapResponse(BaseModel):
    """Tile 2: Fraud velocity over time"""
    hourly_rates: List[HourlyFraudRate]
    peak_attack_window: str
    current_rate: float
    avg_rate: float


class NetworkNode(BaseModel):
    """Network graph node"""
    id: str
    account_id: str
    transaction_count: int
    total_volume: float
    fraud_probability: float
    node_type: str  # "sender", "receiver", "both"


class NetworkEdge(BaseModel):
    """Network graph edge"""
    source: str
    target: str
    transaction_count: int
    total_amount: float
    avg_fraud_probability: float


class FraudRing(BaseModel):
    """Detected fraud ring"""
    ring_id: str
    account_count: int
    transaction_count: int
    total_volume: float
    avg_fraud_probability: float
    accounts: List[str]


class FraudNetworkGraphResponse(BaseModel):
    """Tile 3: Fraud network graph"""
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]
    fraud_rings: List[FraudRing]
    rings_detected: int
    total_accounts: int
    total_volume: float


class FraudTypeStats(BaseModel):
    """Statistics for a fraud type"""
    fraud_type: str
    percentage: float
    count: int
    change_vs_last_week: float
    avg_amount: float


class FraudTypeBreakdownResponse(BaseModel):
    """Tile 4: Fraud type breakdown"""
    fraud_types: List[FraudTypeStats]
    total_fraud_count: int
    dominant_type: str
    emerging_threats: List[str]


class LocationCorridor(BaseModel):
    """High-risk location corridor"""
    from_location: str
    to_location: str
    suspicious_count: int
    fraud_rate: float
    avg_amount: float
    risk_level: RiskLevel


class GeoAnomalyHotspotsResponse(BaseModel):
    """Tile 5: Geographic anomaly hotspots"""
    high_risk_corridors: List[LocationCorridor]
    impossible_travel_count: int
    top_risky_locations: List[Dict[str, Any]]
    heat_map_data: List[Dict[str, Any]]


class AccountAtRisk(BaseModel):
    """Account predicted to be at risk"""
    account_id: str
    fraud_risk: float
    risk_factors: List[str]
    recent_anomalies: List[str]
    recommended_action: str
    last_transaction_time: datetime


class PredictiveRiskScoreResponse(BaseModel):
    """Tile 6: Predictive risk scoring"""
    high_probability_targets: List[AccountAtRisk]
    total_at_risk: int
    risk_distribution: Dict[str, int]
    prediction_confidence: float


class BehavioralAnomaly(BaseModel):
    """Behavioral anomaly detection"""
    anomaly_type: str
    affected_accounts: int
    description: str
    severity: RiskLevel


class BehavioralAnomaliesResponse(BaseModel):
    """Tile 7: Behavioral anomalies"""
    anomalies: List[BehavioralAnomaly]
    total_anomalies: int
    last_updated: datetime


class FeatureImportance(BaseModel):
    """Feature importance for a transaction"""
    feature: str
    importance: float
    description: str


class TransactionExplanation(BaseModel):
    """AI explanation for why transaction was flagged"""
    transaction_id: str
    fraud_probability: float
    feature_importances: List[FeatureImportance]
    explanation: str
    recommended_action: str


class ModelMetrics(BaseModel):
    """Model performance metrics"""
    precision: float
    recall: float
    f1_score: float
    accuracy: float
    auc_roc: float


class ModelHealthDashboardResponse(BaseModel):
    """Tile 11: Model health monitoring"""
    current_metrics: ModelMetrics
    metrics_change: Dict[str, float]
    avg_inference_time_ms: float
    data_drift_status: str
    feature_drift_alerts: List[str]
    recommendation: str
    last_retrain: datetime
    model_version: str


class ConfusionMatrixResponse(BaseModel):
    """Tile 12: Confusion matrix"""
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int
    false_positive_rate: float
    false_negative_rate: float
    cost_impact: float


class FinancialImpactResponse(BaseModel):
    """Tile 14: Financial impact scorecard"""
    fraud_prevented: float
    fraud_losses: float
    prevention_costs: float
    false_positive_impact: float
    net_savings: float
    roi_percentage: float
    period: str


class CustomerExperienceResponse(BaseModel):
    """Tile 15: Customer experience impact"""
    blocked_transactions: int
    false_alarm_rate: float
    avg_review_time_minutes: float
    customer_complaints: int
    churn_rate: float
    satisfaction_score: float


class TimeSeriesPoint(BaseModel):
    """Time series data point"""
    timestamp: datetime
    value: float
    label: Optional[str] = None


class TemporalTrendsResponse(BaseModel):
    """Tile 16: Temporal trends and forecasting"""
    historical_trend: List[TimeSeriesPoint]
    forecast: List[TimeSeriesPoint]
    expected_fraud_volume_change: float
    high_risk_days: List[str]
    emerging_patterns: List[str]


class RiskMatrixCell(BaseModel):
    """Risk matrix cell"""
    channel: str
    category: str
    fraud_rate: float
    transaction_count: int
    risk_level: RiskLevel


class MerchantChannelRiskResponse(BaseModel):
    """Tile 17: Merchant & channel risk matrix"""
    risk_matrix: List[RiskMatrixCell]
    highest_risk_combination: Dict[str, Any]
    recommendations: List[str]


class Alert(BaseModel):
    """Alert item"""
    alert_id: str
    severity: RiskLevel
    title: str
    description: str
    timestamp: datetime
    related_transactions: Optional[List[str]] = None


class SmartAlertFeedResponse(BaseModel):
    """Tile 18: Smart alerts"""
    critical_alerts: List[Alert]
    warning_alerts: List[Alert]
    info_alerts: List[Alert]
    total_unread: int
    last_updated: datetime

