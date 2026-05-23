import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertManager:
    """Manage system alerts"""
    
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            'high_anomaly_rate': 0.2,  # 20% anomaly rate
            'low_quality_score': 60,    # Score below 60
            'high_latency': 1000,       # 1 second
            'error_rate': 0.05          # 5% error rate
        }
    
    def check_anomaly_rate(self, anomaly_rate: float) -> bool:
        """Check if anomaly rate exceeds threshold"""
        if anomaly_rate > self.thresholds['high_anomaly_rate']:
            self.add_alert(
                severity='warning',
                message=f"High anomaly rate detected: {anomaly_rate:.1%}",
                metric='anomaly_rate',
                value=anomaly_rate
            )
            return True
        return False
    
    def check_quality_score(self, avg_score: float) -> bool:
        """Check if quality score is too low"""
        if avg_score < self.thresholds['low_quality_score']:
            self.add_alert(
                severity='critical',
                message=f"Average quality score dropped to {avg_score:.1f}",
                metric='quality_score',
                value=avg_score
            )
            return True
        return False
    
    def check_latency(self, latency_ms: float) -> bool:
        """Check if latency is too high"""
        if latency_ms > self.thresholds['high_latency']:
            self.add_alert(
                severity='warning',
                message=f"High latency detected: {latency_ms:.0f}ms",
                metric='latency',
                value=latency_ms
            )
            return True
        return False
    
    def add_alert(self, severity: str, message: str, metric: str, value: float):
        """Add an alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'message': message,
            'metric': metric,
            'value': value
        }
        self.alerts.append(alert)
        logger.warning(f"Alert: {message}")
    
    def get_alerts(self, limit: int = 10) -> list:
        """Get recent alerts"""
        return self.alerts[-limit:]
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []