"""
Dashboard endpoints - Tier 1 & 2 (Executive Overview & Operational Command Center)
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from backend.models.schemas import (
    ExecutiveOverviewResponse,
    HighRiskTransactionsFeedResponse,
    FraudVelocityHeatmapResponse,
    FraudTypeBreakdownResponse,
    BehavioralAnomaliesResponse,
    SmartAlertFeedResponse
)
from backend.services.fraud_detection import FraudDetectionService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/executive-overview", response_model=ExecutiveOverviewResponse)
async def get_executive_overview(
    hours: int = Query(24, description="Time window in hours", ge=1, le=168)
):
    """
    **TILE 1: Executive Overview** - Real-time fraud pulse KPIs
    
    Returns key metrics for C-Suite and Risk Directors:
    - Total fraud amount in period
    - Fraud rate and trend
    - Amount blocked/prevented
    - Average detection time
    - Pending alerts count
    """
    try:
        data = FraudDetectionService.get_executive_overview(hours=hours)
        return ExecutiveOverviewResponse(**data)
    except Exception as e:
        logger.error(f"Error in executive overview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-risk-transactions", response_model=HighRiskTransactionsFeedResponse)
async def get_high_risk_transactions(
    limit: int = Query(50, description="Maximum transactions to return", ge=1, le=200)
):
    """
    **TILE 2: High-Risk Transactions Live Feed** - Critical alerts requiring action
    
    Returns prioritized list of transactions requiring immediate attention,
    categorized by severity (critical, high, medium priority).
    """
    try:
        data = FraudDetectionService.get_high_risk_transactions(limit=limit)
        return HighRiskTransactionsFeedResponse(**data)
    except Exception as e:
        logger.error(f"Error getting high-risk transactions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fraud-velocity-heatmap", response_model=FraudVelocityHeatmapResponse)
async def get_fraud_velocity_heatmap(
    hours: int = Query(24, description="Time window in hours", ge=1, le=168)
):
    """
    **TILE 3: Fraud Velocity Heatmap** - Hourly fraud rate analysis
    
    Shows fraud patterns by hour to identify peak attack windows.
    Helps with resource allocation and threat anticipation.
    """
    try:
        data = FraudDetectionService.get_fraud_velocity_heatmap(hours=hours)
        return FraudVelocityHeatmapResponse(**data)
    except Exception as e:
        logger.error(f"Error getting fraud velocity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fraud-type-breakdown", response_model=FraudTypeBreakdownResponse)
async def get_fraud_type_breakdown():
    """
    **TILE 4: Fraud Type Breakdown** - Distribution of fraud categories
    
    Analyzes fraud by type (account takeover, money laundering, etc.)
    with week-over-week trends and emerging threats.
    """
    try:
        data = FraudDetectionService.get_fraud_type_breakdown()
        return FraudTypeBreakdownResponse(**data)
    except Exception as e:
        logger.error(f"Error getting fraud type breakdown: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/behavioral-anomalies", response_model=BehavioralAnomaliesResponse)
async def get_behavioral_anomalies():
    """
    **TILE 7: Behavioral Anomalies** - Pattern-based anomaly detection
    
    Detects unusual behavioral patterns:
    - Testing phase (small then large transactions)
    - Device switching
    - Dormant account reactivation
    """
    try:
        data = FraudDetectionService.get_behavioral_anomalies()
        return BehavioralAnomaliesResponse(**data)
    except Exception as e:
        logger.error(f"Error detecting behavioral anomalies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/smart-alerts", response_model=SmartAlertFeedResponse)
async def get_smart_alerts(
    hours: int = Query(24, description="Time window in hours", ge=1, le=168)
):
    """
    **TILE 18: Smart Alert Feed** - Intelligent alert prioritization
    
    Generates and categorizes alerts based on:
    - Fraud rate spikes
    - Network anomalies
    - Model performance issues
    - High transaction volumes
    """
    try:
        data = FraudDetectionService.generate_smart_alerts(hours=hours)
        return SmartAlertFeedResponse(**data)
    except Exception as e:
        logger.error(f"Error generating smart alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

