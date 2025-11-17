"""
Model monitoring endpoints - ML performance tracking
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from backend.models.schemas import (
    ModelHealthDashboardResponse,
    ConfusionMatrixResponse
)
from backend.services.model_monitoring import ModelMonitoringService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/model-health", response_model=ModelHealthDashboardResponse)
async def get_model_health():
    """
    **TILE 11: Model Health Dashboard** - ML model performance monitoring
    
    Tracks:
    - Precision, recall, F1-score, accuracy
    - Metric changes over time
    - Inference latency
    - Data drift detection
    - Feature drift alerts
    - Retraining recommendations
    """
    try:
        data = ModelMonitoringService.get_model_health()
        return ModelHealthDashboardResponse(**data)
    except Exception as e:
        logger.error(f"Error getting model health: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/confusion-matrix", response_model=ConfusionMatrixResponse)
async def get_confusion_matrix():
    """
    **TILE 12: Confusion Matrix Live** - Classification performance breakdown
    
    Shows:
    - True Positives (correctly flagged fraud)
    - True Negatives (correctly cleared legitimate)
    - False Positives (false alarms)
    - False Negatives (missed fraud)
    - False positive/negative rates
    - Cost impact analysis
    """
    try:
        data = ModelMonitoringService.get_confusion_matrix()
        return ConfusionMatrixResponse(**data)
    except Exception as e:
        logger.error(f"Error getting confusion matrix: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feature-importance", response_model=List[Dict[str, Any]])
async def get_feature_importance():
    """
    **Global Feature Importance** - Which features drive predictions?
    
    Returns feature importance scores across all predictions
    to understand which signals matter most for fraud detection.
    """
    try:
        importances = ModelMonitoringService.get_feature_importance_global()
        return importances
    except Exception as e:
        logger.error(f"Error getting feature importance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

