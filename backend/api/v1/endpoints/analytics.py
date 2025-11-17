"""
Analytics endpoints - Geographic, temporal, and business intelligence
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
import logging

from backend.models.schemas import (
    GeoAnomalyHotspotsResponse,
    PredictiveRiskScoreResponse,
    FinancialImpactResponse,
    CustomerExperienceResponse,
    TemporalTrendsResponse,
    MerchantChannelRiskResponse,
    TransactionExplanation
)
from backend.services.analytics import AnalyticsService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/geo-anomaly-hotspots", response_model=GeoAnomalyHotspotsResponse)
async def get_geo_anomaly_hotspots():
    """
    **TILE 5: Geo-Anomaly Hotspots** - Geographic fraud analysis
    
    Identifies:
    - High-risk location corridors
    - Impossible travel patterns
    - Top risky locations
    - Heat map data for visualization
    """
    try:
        data = AnalyticsService.get_geo_anomaly_hotspots()
        return GeoAnomalyHotspotsResponse(**data)
    except Exception as e:
        logger.error(f"Error getting geo anomalies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictive-risk-scores", response_model=PredictiveRiskScoreResponse)
async def get_predictive_risk_scores(
    limit: int = Query(127, description="Maximum accounts to return", ge=1, le=500)
):
    """
    **TILE 6: Predictive Risk Scores** - Accounts at risk in next 24 hours
    
    Uses behavioral indicators to predict which accounts are likely
    to be compromised, enabling proactive protection.
    """
    try:
        data = AnalyticsService.get_predictive_risk_scores(limit=limit)
        return PredictiveRiskScoreResponse(**data)
    except Exception as e:
        logger.error(f"Error getting predictive risk scores: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/financial-impact", response_model=FinancialImpactResponse)
async def get_financial_impact(
    period_days: int = Query(30, description="Period in days", ge=1, le=365)
):
    """
    **TILE 14: Financial Impact Scorecard** - ROI and cost analysis
    
    Calculates:
    - Fraud prevented vs losses
    - Prevention costs
    - False positive impact
    - Net savings and ROI
    """
    try:
        data = AnalyticsService.get_financial_impact(period_days=period_days)
        return FinancialImpactResponse(**data)
    except Exception as e:
        logger.error(f"Error calculating financial impact: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-experience", response_model=CustomerExperienceResponse)
async def get_customer_experience():
    """
    **TILE 15: Customer Experience Impact** - User satisfaction metrics
    
    Monitors impact of fraud detection on legitimate users:
    - Blocked transactions
    - False alarm rate
    - Customer complaints
    - Churn rate
    """
    try:
        data = AnalyticsService.get_customer_experience_metrics()
        return CustomerExperienceResponse(**data)
    except Exception as e:
        logger.error(f"Error getting customer experience metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/temporal-trends", response_model=TemporalTrendsResponse)
async def get_temporal_trends(
    months: int = Query(12, description="Historical months", ge=1, le=24)
):
    """
    **TILE 16: Temporal Trends & Forecasting** - Time series analysis
    
    Provides:
    - Historical fraud trends
    - 30-day forecast
    - High-risk days identification
    - Emerging pattern detection
    """
    try:
        data = AnalyticsService.get_temporal_trends(months=months)
        return TemporalTrendsResponse(**data)
    except Exception as e:
        logger.error(f"Error getting temporal trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/merchant-channel-risk", response_model=MerchantChannelRiskResponse)
async def get_merchant_channel_risk():
    """
    **TILE 17: Merchant & Channel Risk Matrix** - Cross-sectional risk analysis
    
    Analyzes fraud rates across:
    - Payment channels (mobile, web, ATM, POS)
    - Merchant categories (retail, travel, utilities, etc.)
    Provides actionable recommendations.
    """
    try:
        data = AnalyticsService.get_merchant_channel_risk()
        return MerchantChannelRiskResponse(**data)
    except Exception as e:
        logger.error(f"Error getting merchant/channel risk: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transaction-explanation/{transaction_id}", response_model=TransactionExplanation)
async def explain_transaction(
    transaction_id: str = Path(..., description="Transaction ID to explain")
):
    """
    **TILE 10: Feature Importance Explainer** - AI explanation for flagged transaction
    
    Provides interpretable explanation of why a specific transaction
    was flagged, including feature importances and recommended action.
    """
    try:
        data = AnalyticsService.explain_transaction(transaction_id)
        
        if 'error' in data:
            raise HTTPException(status_code=404, detail=data['error'])
        
        return TransactionExplanation(**data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error explaining transaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

