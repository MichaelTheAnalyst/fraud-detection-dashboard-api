"""
Network analysis endpoints - Fraud rings and account relationships
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
import logging

from backend.models.schemas import FraudNetworkGraphResponse
from backend.services.network_analysis import NetworkAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/fraud-network-graph", response_model=FraudNetworkGraphResponse)
async def get_fraud_network_graph(
    min_transactions: int = Query(3, description="Minimum transactions to include connection", ge=1, le=10),
    min_fraud_prob: float = Query(0.6, description="Minimum fraud probability", ge=0.0, le=1.0)
):
    """
    **TILE 3: Fraud Network Graph** - Account relationship visualization
    
    Builds graph of suspicious account relationships to identify:
    - Fraud rings (circular transaction patterns)
    - Connected accounts
    - Money flow patterns
    - Network statistics
    
    Returns nodes (accounts) and edges (transactions) for graph visualization.
    """
    try:
        data = NetworkAnalysisService.get_fraud_network_graph(
            min_transactions=min_transactions,
            min_fraud_prob=min_fraud_prob
        )
        return FraudNetworkGraphResponse(**data)
    except Exception as e:
        logger.error(f"Error building fraud network graph: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mule-accounts", response_model=List[Dict[str, Any]])
async def detect_mule_accounts(
    min_senders: int = Query(5, description="Minimum unique senders", ge=3, le=20),
    redistribution_threshold: float = Query(0.8, description="Min redistribution ratio", ge=0.5, le=1.0)
):
    """
    **Money Mule Detection** - Identify accounts used for money laundering
    
    Detects accounts that:
    - Receive funds from many sources
    - Quickly redistribute to other accounts
    - Show high pass-through behavior
    
    These patterns indicate potential money mule activity.
    """
    try:
        mule_accounts = NetworkAnalysisService.detect_mule_accounts(
            min_senders=min_senders,
            redistribution_threshold=redistribution_threshold
        )
        return mule_accounts
    except Exception as e:
        logger.error(f"Error detecting mule accounts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

