from prometheus_client import Counter, Histogram, Gauge, generate_latest
from typing import Dict, Any
import time
import logging

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collect and expose metrics"""
    
    def __init__(self):
        # Validation counters
        self.validations_total = Counter(
            'validations_total',
            'Total number of validations',
            ['status']
        )
        
        self.anomalies_detected = Counter(
            'anomalies_detected_total',
            'Total number of anomalies detected',
            ['type']
        )
        
        # Processing time histogram
        self.processing_time = Histogram(
            'validation_processing_seconds',
            'Validation processing time in seconds',
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0]
        )
        
        # Quality score gauge
        self.quality_score_gauge = Gauge(
            'validation_quality_score',
            'Current average quality score'
        )
        
        # Active validations
        self.active_validations = Gauge(
            'active_validations',
            'Number of active validations'
        )
        
        self.scores = []
    
    def record_validation(self, status: str, processing_time: float, score: float):
        """Record validation metrics"""
        self.validations_total.labels(status=status).inc()
        self.processing_time.observe(processing_time / 1000)  # Convert to seconds
        self.scores.append(score)
        
        # Update average score
        if self.scores:
            self.quality_score_gauge.set(sum(self.scores[-100:]) / len(self.scores[-100:]))
    
    def record_anomaly(self, anomaly_type: str):
        """Record anomaly detection"""
        self.anomalies_detected.labels(type=anomaly_type).inc()
    
    def record_error(self):
        """Record error"""
        self.validations_total.labels(status='error').inc()
    
    def get_metrics(self):
        """Get current metrics"""
        return generate_latest()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return {
            'total_validations': self.validations_total._value.get(),
            'avg_quality_score': self.quality_score_gauge._value.get() if self.scores else 0,
            'anomalies_by_type': {
                k: v._value.get() 
                for k, v in self.anomalies_detected._metrics.items()
            }
        }