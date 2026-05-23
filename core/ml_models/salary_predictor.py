import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class SalaryPredictor:
    """Predict expected salary based on features"""
    
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def extract_features(self, submission: Dict) -> np.ndarray:
        """Extract features for prediction"""
        features = []
        
        # Experience
        features.append(min(submission.get('yearsOfExperience', 0), 20))
        
        # Level
        level = submission.get('level', 'IC3')
        level_num = int(level.replace('IC', '')) if 'IC' in level else 3
        features.append(level_num)
        
        # Location factor
        location = submission.get('location', '')
        if 'India' in location:
            features.append(0.3)
        elif 'USA' in location:
            features.append(1.0)
        else:
            features.append(0.5)
        
        return np.array(features)
    
    def predict(self, submission: Dict) -> Tuple[float, float]:
        """Predict expected salary"""
        features = self.extract_features(submission)
        
        if self.is_trained:
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            predicted = self.model.predict(features_scaled)[0]
            confidence = 0.85
        else:
            # Simple rule-based prediction
            base = submission.get('baseSalary', 50000)
            predicted = base
            confidence = 0.6
        
        return predicted, confidence