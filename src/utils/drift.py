"""
Modulo per calcolo di drift su distribuzioni di label.
"""
import numpy as np
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def kl_divergence(p: Dict[str, float], q: Dict[str, float]) -> float:
    """Calcola la divergenza di Kullback-Leibler tra due distribuzioni discrete."""
    labels = set(p.keys()) | set(q.keys())
    if not labels:
        return 0.0
    
    p_norm = np.array([p.get(label, 1e-10) for label in sorted(labels)])
    q_norm = np.array([q.get(label, 1e-10) for label in sorted(labels)])
    
    p_norm = p_norm / (p_norm.sum() + 1e-10)
    q_norm = q_norm / (q_norm.sum() + 1e-10)
    
    epsilon = 1e-10
    p_norm = np.clip(p_norm, epsilon, 1.0)
    q_norm = np.clip(q_norm, epsilon, 1.0)
    
    kl = np.sum(p_norm * np.log(p_norm / q_norm))
    
    return float(kl)


def windowed_label_distribution(labels: List[str], window_size: int) -> List[Dict[str, float]]:
    """Calcola distribuzioni mobili di label su finestre temporali."""
    if not labels or window_size <= 0:
        return []
    
    distributions = []
    
    for i in range(len(labels)):
        start = max(0, i - window_size + 1)
        window_labels = labels[start:i+1]
        
        label_counts: Dict[str, int] = {}
        total = len(window_labels)
        
        for label in window_labels:
            label_counts[label] = label_counts.get(label, 0) + 1
        
        dist = {label: count / total for label, count in label_counts.items()}
        distributions.append(dist)
    
    return distributions


def compute_reference_distribution(labels: List[str]) -> Dict[str, float]:
    """Calcola la distribuzione di riferimento (baseline) da una lista di label."""
    if not labels:
        return {"negative": 0.33, "neutral": 0.34, "positive": 0.33}
    
    label_counts: Dict[str, int] = {}
    total = len(labels)
    
    for label in labels:
        label_counts[label] = label_counts.get(label, 0) + 1
    
    return {label: count / total for label, count in label_counts.items()}


