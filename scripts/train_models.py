#!/usr/bin/env python
"""Train ML models on historical data"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ml_models.anomaly_detector import CompensationAnomalyDetector
from core.ml_models.fraud_detector import FraudDetectionModel
from database.models import DatabaseManager
import numpy as np
import json

async def train_models():
    """Train all ML models"""
    print("Training ML models...")
    
    # Load historical data
    db = DatabaseManager("sqlite:///levels.db")
    await db.initialize()
    
    historical_data = await db.get_historical_submissions(limit=10000)
    
    if not historical_data:
        print("No historical data found. Using default models.")
        return
    
    # Train anomaly detector
    print(f"Training anomaly detector on {len(historical_data)} samples...")
    anomaly_detector = CompensationAnomalyDetector()
    anomaly_detector.fit(historical_data)
    
    # Save model
    import joblib
    joblib.dump(anomaly_detector, "models/anomaly_detector.pkl")
    
    print("Models trained and saved successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(train_models())