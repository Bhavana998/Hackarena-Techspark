"""Machine learning models"""

from .anomaly_detector import CompensationAnomalyDetector
from .fraud_detector import FraudDetectionModel
from .salary_predictor import SalaryPredictor

__all__ = [
    'CompensationAnomalyDetector',
    'FraudDetectionModel',
    'SalaryPredictor'
]