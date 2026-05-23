import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import logging

logger = logging.getLogger(__name__)

class FraudDetectionModel:
    """Fraud detection model for compensation submissions"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def extract_features(self, submission: Dict, user_history: Dict = None) -> np.ndarray:
        """Extract features for fraud detection"""
        features = []
        
        # Submission velocity
        features.append(user_history.get('submissions_last_hour', 0) if user_history else 0)
        
        # Data consistency
        base = submission.get('baseSalary', 0)
        bonus = submission.get('avgAnnualBonusValue', 0)
        stock = submission.get('avgAnnualStockGrantValue', 0)
        
        features.append(bonus / max(base, 1))
        features.append(stock / max(base, 1))
        
        # Round number indicator
        is_round = (base % 10000 == 0) or (bonus % 10000 == 0)
        features.append(1 if is_round else 0)
        
        # Missing fields
        required_fields = ['company', 'title', 'level', 'location']
        missing = sum(1 for f in required_fields if not submission.get(f))
        features.append(missing)
        
        return np.array(features)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train fraud detection model"""
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        logger.info("Fraud detection model trained")
    
    def predict(self, submission: Dict, user_history: Dict = None) -> Tuple[float, float]:
        """Predict fraud probability"""
        features = self.extract_features(submission, user_history)
        
        if self.is_trained:
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            fraud_prob = self.model.predict_proba(features_scaled)[0][1]
            confidence = 0.8
        else:
            fraud_prob = self._rule_based_score(submission, user_history)
            confidence = 0.6
        
        return fraud_prob, confidence
    
    def _rule_based_score(self, submission: Dict, user_history: Dict = None) -> float:
        """Fallback rule-based detection"""
        score = 0.0
        
        if user_history and user_history.get('submissions_last_hour', 0) > 5:
            score += 0.3
        
        if submission.get('baseSalary', 0) > 500000:
            score += 0.3
        
        return min(score, 1.0)