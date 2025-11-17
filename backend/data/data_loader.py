"""
Data loading and caching layer for efficient CSV operations
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from functools import lru_cache
import logging

from backend.config import settings

logger = logging.getLogger(__name__)


class DataLoader:
    """Singleton class for loading and caching fraud detection data"""
    
    _instance = None
    _data: Optional[pd.DataFrame] = None
    _loaded_at: Optional[datetime] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance
    
    def load_data(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load data from CSV with caching
        
        Args:
            force_reload: Force reload from disk
            
        Returns:
            DataFrame with all transaction data
        """
        if self._data is not None and not force_reload:
            logger.info("Returning cached data")
            return self._data
        
        logger.info(f"Loading data from {settings.DATA_FILE_PATH}")
        
        try:
            # Load with optimized dtypes for memory efficiency
            dtype_spec = {
                'transaction_id': 'string',
                'sender_account': 'string',
                'receiver_account': 'string',
                'transaction_type': 'category',
                'merchant_category': 'category',
                'location': 'category',
                'device_used': 'category',
                'is_fraud': 'bool',
                'fraud_type': 'string',
                'payment_channel': 'category',
                'ip_address': 'string',
                'device_hash': 'string',
                'amount': 'float32',
                'time_since_last_transaction': 'float32',
                'spending_deviation_score': 'float32',
                'velocity_score': 'float32',
                'geo_anomaly_score': 'float32'
            }
            
            self._data = pd.read_csv(
                settings.DATA_FILE_PATH,
                dtype=dtype_spec,
                parse_dates=['timestamp']
            )
            
            # Data preprocessing
            self._data = self._preprocess_data(self._data)
            
            self._loaded_at = datetime.now()
            logger.info(f"Data loaded successfully: {len(self._data):,} rows")
            
            return self._data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data for analysis
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        # Add derived columns
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['date'] = df['timestamp'].dt.date
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        df['is_night'] = df['hour'].between(0, 6)
        
        # Calculate fraud probability (simulated from behavioral features)
        df['fraud_probability'] = (
            df['velocity_score'] * 0.34 +
            df['geo_anomaly_score'] * 0.28 +
            df['spending_deviation_score'] * 0.19 +
            (df['time_since_last_transaction'] < 60).astype(float) * 0.11 +
            np.random.uniform(0, 0.08, len(df))  # Random factor
        ).clip(0, 1)
        
        # Risk categories
        df['risk_category'] = pd.cut(
            df['fraud_probability'],
            bins=[0, 0.3, 0.6, 0.75, 1.0],
            labels=['low', 'medium', 'high', 'critical']
        )
        
        return df
    
    def get_data(self) -> pd.DataFrame:
        """Get cached data or load if not available"""
        if self._data is None:
            return self.load_data()
        return self._data
    
    def get_recent_transactions(self, hours: int = 24) -> pd.DataFrame:
        """Get transactions from the last N hours"""
        df = self.get_data()
        cutoff = df['timestamp'].max() - timedelta(hours=hours)
        return df[df['timestamp'] >= cutoff]
    
    def get_high_risk_transactions(self, threshold: float = 0.75, limit: int = 100) -> pd.DataFrame:
        """Get high-risk transactions above threshold"""
        df = self.get_data()
        high_risk = df[df['fraud_probability'] >= threshold].copy()
        return high_risk.nlargest(limit, 'fraud_probability')
    
    def get_fraud_transactions(self) -> pd.DataFrame:
        """Get all fraudulent transactions"""
        df = self.get_data()
        return df[df['is_fraud'] == True]
    
    @property
    def data_info(self) -> Dict[str, Any]:
        """Get information about loaded data"""
        if self._data is None:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "rows": len(self._data),
            "loaded_at": self._loaded_at.isoformat() if self._loaded_at else None,
            "date_range": {
                "start": self._data['timestamp'].min().isoformat(),
                "end": self._data['timestamp'].max().isoformat()
            },
            "fraud_count": int(self._data['is_fraud'].sum()),
            "fraud_rate": float(self._data['is_fraud'].mean())
        }


# Global instance
data_loader = DataLoader()

