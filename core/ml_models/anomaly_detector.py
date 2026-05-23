import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from typing import Dict, List, Tuple, Any
import torch
import torch.nn as nn
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepAnomalyDetector(nn.Module):
    """PyTorch autoencoder for deep anomaly detection"""
    
    def __init__(self, input_dim: int, hidden_dims: List[int] = [128, 64, 32]):
        super().__init__()
        
        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = h_dim
        
        self.encoder = nn.Sequential(*encoder_layers)
        
        # Decoder
        decoder_layers = []
        for h_dim in reversed(hidden_dims[:-1]):
            decoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU()
            ])
            prev_dim = h_dim
        
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        self.decoder = nn.Sequential(*decoder_layers)
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def reconstruction_error(self, x):
        with torch.no_grad():
            reconstructed = self(x)
            mse = torch.mean((x - reconstructed) ** 2, dim=1)
        return mse.numpy()

class CompensationAnomalyDetector:
    """Specialized anomaly detector for compensation data"""
    
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=200,
            max_samples='auto'
        )
        self.lof = LocalOutlierFactor(contamination=0.1, novelty=True)
        self.deep_detector = None
        self.scaler = StandardScaler()
        self.is_fitted = False
        
        # Industry benchmarks
        self.level_benchmarks = {
            'IC1': {'min': 15000, 'max': 35000, 'typical': 25000},
            'IC2': {'min': 25000, 'max': 50000, 'typical': 38000},
            'IC3': {'min': 40000, 'max': 80000, 'typical': 60000},
            'IC4': {'min': 60000, 'max': 120000, 'typical': 90000},
            'IC5': {'min': 90000, 'max': 180000, 'typical': 135000},
            'IC6': {'min': 130000, 'max': 250000, 'typical': 190000}
        }
    
    def extract_features(self, submission: Dict) -> np.ndarray:
        """Extract numerical features from submission"""
        features = []
        
        # Base compensation features
        base_salary = submission.get('baseSalary', 0)
        features.append(np.log1p(base_salary))
        
        # Total compensation
        total_comp = submission.get('totalCompensation', 0)
        features.append(np.log1p(total_comp))
        
        # Stock features
        stock_value = submission.get('avgAnnualStockGrantValue', 0)
        features.append(np.log1p(stock_value))
        
        # Bonus features
        bonus_value = submission.get('avgAnnualBonusValue', 0)
        features.append(np.log1p(bonus_value))
        
        # Ratios
        if base_salary > 0:
            bonus_ratio = bonus_value / base_salary
            stock_ratio = stock_value / base_salary
            features.append(bonus_ratio)
            features.append(stock_ratio)
        else:
            features.extend([0, 0])
        
        # Experience
        years_exp = submission.get('yearsOfExperience', 0)
        features.append(min(years_exp, 20))
        
        # Level seniority
        level = submission.get('level', 'IC1')
        level_num = int(level.replace('IC', '')) if 'IC' in level else 3
        features.append(level_num / 10)
        
        return np.array(features)
    
    def fit(self, historical_data: List[Dict]):
        """Train detector on historical data"""
        if len(historical_data) < 100:
            logger.warning(f"Only {len(historical_data)} samples available for training")
            return
        
        X = np.vstack([self.extract_features(d) for d in historical_data])
        X_scaled = self.scaler.fit_transform(X)
        
        self.isolation_forest.fit(X_scaled)
        self.lof.fit(X_scaled)
        
        if len(historical_data) > 500:
            self._train_deep_autoencoder(X_scaled)
        
        self.is_fitted = True
        logger.info(f"Anomaly detector trained on {len(historical_data)} samples")
    
    def _train_deep_autoencoder(self, X: np.ndarray, epochs: int = 100):
        """Train deep learning autoencoder"""
        input_dim = X.shape[1]
        self.deep_detector = DeepAnomalyDetector(input_dim=input_dim)
        optimizer = torch.optim.Adam(self.deep_detector.parameters(), lr=0.001)
        
        X_tensor = torch.FloatTensor(X)
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            reconstructed = self.deep_detector(X_tensor)
            loss = nn.MSELoss()(reconstructed, X_tensor)
            loss.backward()
            optimizer.step()
    
    def detect(self, submission: Dict) -> Dict[str, Any]:
        """Detect anomalies in submission"""
        features = self.extract_features(submission)
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        if_scores = self.isolation_forest.score_samples(features_scaled)
        lof_scores = self.lof.score_samples(features_scaled)
        
        anomaly_score = (1 - (if_scores[0] + 0.5) / 1.5) * 0.5 + \
                       (1 - (lof_scores[0] + 0.5) / 1.5) * 0.5
        
        if self.deep_detector:
            with torch.no_grad():
                reconstruction_error = self.deep_detector.reconstruction_error(
                    torch.FloatTensor(features_scaled)
                )
                deep_score = np.clip(reconstruction_error[0] / 0.1, 0, 1)
                anomaly_score = anomaly_score * 0.6 + deep_score * 0.4
        
        rule_issues = self._rule_based_checks(submission)
        
        is_anomaly = anomaly_score > 0.7 or len(rule_issues) > 0
        
        return {
            'is_anomaly': is_anomaly,
            'anomaly_score': float(anomaly_score),
            'confidence': float(1 - abs(anomaly_score - 0.5) * 2),
            'rule_issues': rule_issues,
            'explanation': self._generate_explanation(submission, anomaly_score, rule_issues)
        }
    
    def _rule_based_checks(self, submission: Dict) -> List[Dict]:
        """Apply rule-based anomaly detection"""
        issues = []
        
        base_salary = submission.get('baseSalary', 0)
        level = submission.get('level', 'IC1')
        
        benchmark = self.level_benchmarks.get(level, self.level_benchmarks['IC3'])
        
        if base_salary < benchmark['min'] * 0.7:
            issues.append({
                'type': 'salary_too_low',
                'severity': 'high',
                'message': f"Base salary ${base_salary:,.0f} is significantly below market rate"
            })
        elif base_salary > benchmark['max'] * 1.5:
            issues.append({
                'type': 'salary_too_high',
                'severity': 'high',
                'message': f"Base salary ${base_salary:,.0f} is unusually high"
            })
        
        return issues
    
    def _generate_explanation(self, submission: Dict, anomaly_score: float, rule_issues: List) -> str:
        """Generate human-readable explanation"""
        if not rule_issues and anomaly_score < 0.6:
            return "Submission appears normal based on market patterns"
        
        explanations = []
        if anomaly_score > 0.8:
            explanations.append("EXTREME statistical anomaly detected")
        elif anomaly_score > 0.6:
            explanations.append("Statistical outlier detected")
        
        for issue in rule_issues[:2]:
            explanations.append(issue['message'])
        
        return " | ".join(explanations)