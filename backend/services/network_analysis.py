"""
Network analysis for fraud ring detection
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict, deque
from datetime import datetime, timedelta
import logging

from backend.data.data_loader import data_loader
from backend.models.schemas import NetworkNode, NetworkEdge, FraudRing

logger = logging.getLogger(__name__)


class NetworkAnalysisService:
    """Service for network and graph analysis"""
    
    @staticmethod
    def get_fraud_network_graph(min_transactions: int = 3, 
                                 min_fraud_prob: float = 0.6) -> Dict[str, Any]:
        """
        Build fraud network graph
        
        Args:
            min_transactions: Minimum transactions to include connection
            min_fraud_prob: Minimum fraud probability threshold
            
        Returns:
            Network graph with nodes, edges, and detected rings
        """
        df = data_loader.get_data()
        
        # Filter to suspicious transactions
        suspicious = df[df['fraud_probability'] >= min_fraud_prob].copy()
        
        # Build transaction pairs
        pairs = suspicious.groupby(['sender_account', 'receiver_account']).agg({
            'transaction_id': 'count',
            'amount': 'sum',
            'fraud_probability': 'mean'
        }).reset_index()
        
        pairs.columns = ['sender', 'receiver', 'transaction_count', 'total_amount', 'avg_fraud_prob']
        pairs = pairs[pairs['transaction_count'] >= min_transactions]
        
        # Build nodes
        nodes_dict = NetworkAnalysisService._build_nodes(suspicious, pairs)
        
        # Build edges
        edges = []
        for _, row in pairs.iterrows():
            edges.append(NetworkEdge(
                source=row['sender'],
                target=row['receiver'],
                transaction_count=int(row['transaction_count']),
                total_amount=float(row['total_amount']),
                avg_fraud_probability=float(row['avg_fraud_prob'])
            ))
        
        # Detect fraud rings
        fraud_rings = NetworkAnalysisService._detect_fraud_rings(pairs, suspicious)
        
        # Calculate summary stats
        total_volume = float(pairs['total_amount'].sum())
        total_accounts = len(nodes_dict)
        
        return {
            'nodes': list(nodes_dict.values()),
            'edges': edges[:200],  # Limit for visualization
            'fraud_rings': fraud_rings,
            'rings_detected': len(fraud_rings),
            'total_accounts': total_accounts,
            'total_volume': round(total_volume, 2)
        }
    
    @staticmethod
    def _build_nodes(df: pd.DataFrame, pairs: pd.DataFrame) -> Dict[str, NetworkNode]:
        """Build network nodes from transactions"""
        nodes = {}
        
        # Get all accounts involved
        all_accounts = set(pairs['sender'].unique()) | set(pairs['receiver'].unique())
        
        for account in all_accounts:
            # Get account statistics
            sent = df[df['sender_account'] == account]
            received = df[df['receiver_account'] == account]
            
            transaction_count = len(sent) + len(received)
            total_volume = float(sent['amount'].sum() + received['amount'].sum())
            
            # Determine node type
            if len(sent) > 0 and len(received) > 0:
                node_type = "both"
            elif len(sent) > 0:
                node_type = "sender"
            else:
                node_type = "receiver"
            
            # Calculate average fraud probability
            all_txns = pd.concat([sent, received])
            avg_fraud_prob = float(all_txns['fraud_probability'].mean()) if len(all_txns) > 0 else 0.0
            
            nodes[account] = NetworkNode(
                id=account,
                account_id=account,
                transaction_count=transaction_count,
                total_volume=round(total_volume, 2),
                fraud_probability=round(avg_fraud_prob, 3),
                node_type=node_type
            )
        
        return nodes
    
    @staticmethod
    def _detect_fraud_rings(pairs: pd.DataFrame, df: pd.DataFrame) -> List[FraudRing]:
        """
        Detect fraud rings using graph algorithms
        
        Args:
            pairs: Transaction pairs DataFrame
            df: Original transaction data
            
        Returns:
            List of detected fraud rings
        """
        # Build adjacency list
        graph = defaultdict(set)
        for _, row in pairs.iterrows():
            graph[row['sender']].add(row['receiver'])
        
        # Find strongly connected components (potential rings)
        rings = []
        visited = set()
        ring_id = 1
        
        for start_node in graph.keys():
            if start_node in visited:
                continue
            
            # BFS to find connected components
            component = NetworkAnalysisService._find_connected_component(
                start_node, graph, visited
            )
            
            if len(component) >= 3:  # Ring needs at least 3 accounts
                # Check if it's actually a ring (cyclic)
                if NetworkAnalysisService._is_cyclic(component, graph):
                    # Calculate ring statistics
                    ring_txns = df[
                        df['sender_account'].isin(component) &
                        df['receiver_account'].isin(component)
                    ]
                    
                    rings.append(FraudRing(
                        ring_id=f"RING_{ring_id:03d}",
                        account_count=len(component),
                        transaction_count=len(ring_txns),
                        total_volume=float(ring_txns['amount'].sum()),
                        avg_fraud_probability=float(ring_txns['fraud_probability'].mean()),
                        accounts=list(component)[:10]  # Limit to 10 for display
                    ))
                    ring_id += 1
        
        return rings[:10]  # Return top 10 rings
    
    @staticmethod
    def _find_connected_component(start: str, graph: Dict, visited: Set) -> Set[str]:
        """Find connected component using BFS"""
        component = set()
        queue = deque([start])
        
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            
            visited.add(node)
            component.add(node)
            
            # Add neighbors
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return component
    
    @staticmethod
    def _is_cyclic(component: Set[str], graph: Dict) -> bool:
        """Check if component contains cycles"""
        # Simple check: if any node in component points to another in component
        for node in component:
            neighbors = graph.get(node, set())
            if any(n in component and n != node for n in neighbors):
                return True
        return False
    
    @staticmethod
    def detect_mule_accounts(min_senders: int = 5, 
                            redistribution_threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Detect potential mule accounts
        
        Args:
            min_senders: Minimum number of senders to flag as mule
            redistribution_threshold: Ratio of money in vs money out
            
        Returns:
            List of potential mule accounts
        """
        df = data_loader.get_data()
        
        # Get accounts that receive from many and send to many
        received = df.groupby('receiver_account').agg({
            'sender_account': 'nunique',
            'amount': 'sum',
            'fraud_probability': 'mean'
        }).reset_index()
        received.columns = ['account', 'unique_senders', 'amount_received', 'avg_fraud_prob']
        
        sent = df.groupby('sender_account').agg({
            'receiver_account': 'nunique',
            'amount': 'sum'
        }).reset_index()
        sent.columns = ['account', 'unique_receivers', 'amount_sent']
        
        # Merge
        mule_candidates = received.merge(sent, on='account', how='inner')
        
        # Filter: many senders, quick redistribution
        mule_candidates['redistribution_ratio'] = (
            mule_candidates['amount_sent'] / mule_candidates['amount_received']
        ).fillna(0)
        
        mules = mule_candidates[
            (mule_candidates['unique_senders'] >= min_senders) &
            (mule_candidates['redistribution_ratio'] >= redistribution_threshold)
        ]
        
        return mules.head(20).to_dict('records')

