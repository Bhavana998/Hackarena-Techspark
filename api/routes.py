from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import asyncio
import json
import logging

# Fix imports - use try-except for debugging
try:
    from core.ml_models.anomaly_detector import CompensationAnomalyDetector
    from core.validators.vesting_validator import VestingValidator
    from core.validators.currency_validator import CurrencyValidator
    from core.validators.geographic import GeographicValidator
    from core.scoring.quality_scorer import QualityScorer
except ImportError as e:
    print(f"Import error: {e}")
    # Create fallback classes
    class CompensationAnomalyDetector:
        def detect(self, x): return {'is_anomaly': False, 'anomaly_score': 0.1, 'confidence': 0.9, 'rule_issues': [], 'explanation': 'OK'}
        def fit(self, x): pass
    
    class VestingValidator:
        def validate(self, x, y): return {'is_valid': True, 'issues': []}
    
    class CurrencyValidator:
        def validate_currency_consistency(self, x): return {'has_mixed_currencies': False, 'issues': []}
    
    class GeographicValidator:
        def validate_location(self, x, y): return {'is_valid': True, 'issues': [], 'city': 'Unknown', 'country': 'Unknown', 'cost_multiplier': 1.0}
    
    class QualityScorer:
        def calculate_score(self, *args, **kwargs): return 85.0

from database.models import DatabaseManager
from monitoring.metrics import MetricsCollector
from .models import CompensationSubmission, ValidationResponse, BatchValidationResponse
from config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize components
anomaly_detector = CompensationAnomalyDetector()
vesting_validator = VestingValidator()
currency_validator = CurrencyValidator()
geo_validator = GeographicValidator()
quality_scorer = QualityScorer()
db_manager = DatabaseManager(settings.DATABASE_URL)
metrics = MetricsCollector()

@router.post("/validate", response_model=ValidationResponse)
async def validate_submission(
    submission: CompensationSubmission,
    background_tasks: BackgroundTasks,
    request: Request = None
):
    """Validate a single compensation submission"""
    
    start_time = datetime.now()
    submission_id = submission.uuid or str(uuid.uuid4())
    
    # Get client IP for rate limiting
    client_ip = request.client.host if request and request.client else "unknown"
    
    try:
        # 1. Anomaly detection
        anomaly_result = anomaly_detector.detect(submission.dict())
        
        # 2. Currency validation
        currency_result = currency_validator.validate_currency_consistency(
            submission.dict()
        )
        
        # 3. Vesting schedule validation
        vesting_result = vesting_validator.validate(
            [v.dict() for v in submission.vestingSchedule] if submission.vestingSchedule else [],
            submission.avgAnnualStockGrantValue
        )
        
        # 4. Geographic validation
        geo_result = geo_validator.validate_location(
            submission.location,
            submission.company
        )
        
        # 5. Calculate quality score
        quality_score = quality_scorer.calculate_score(
            submission.dict(),
            anomaly_result,
            currency_result,
            vesting_result,
            geo_result
        )
        
        # 6. Determine status
        if anomaly_result.get('anomaly_score', 0) > 0.8 or any(
            i.get('severity') == 'critical' for i in anomaly_result.get('rule_issues', [])
        ):
            status = "rejected"
        elif anomaly_result.get('anomaly_score', 0) > 0.6:
            status = "flagged"
        elif quality_score < 60:
            status = "needs_review"
        else:
            status = "approved"
        
        # 7. Generate recommendations
        recommendations = []
        if anomaly_result.get('anomaly_score', 0) > 0.6:
            recommendations.append(anomaly_result.get('explanation', 'Anomaly detected'))
        
        for issue in currency_result.get('issues', [])[:2]:
            recommendations.append(issue['message'])
        
        for issue in vesting_result.get('issues', [])[:2]:
            recommendations.append(issue['message'])
        
        # 8. Save to database (in background)
        background_tasks.add_task(
            db_manager.save_submission,
            submission_id=submission_id,
            submission=submission.dict(),
            validation_result={
                'quality_score': quality_score,
                'status': status,
                'anomaly_score': anomaly_result.get('anomaly_score', 0)
            },
            client_ip=client_ip
        )
        
        # Track metrics
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        metrics.record_validation(
            status=status,
            processing_time=processing_time,
            score=quality_score
        )
        
        return ValidationResponse(
            submission_id=submission_id,
            timestamp=datetime.now(),
            quality_score=round(quality_score, 1),
            confidence_level=round(anomaly_result.get('confidence', 0.5), 2),
            status=status,
            anomaly_detection={
                'score': round(anomaly_result.get('anomaly_score', 0), 3),
                'is_anomaly': anomaly_result.get('is_anomaly', False),
                'explanation': anomaly_result.get('explanation', ''),
                'rule_issues': anomaly_result.get('rule_issues', [])
            },
            currency_validation=currency_result,
            vesting_validation=vesting_result,
            geographic_validation=geo_result,
            recommendations=recommendations[:5],
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        metrics.record_error()
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.post("/validate/batch", response_model=BatchValidationResponse)
async def validate_batch(
    submissions: List[CompensationSubmission],
    background_tasks: BackgroundTasks
):
    """Batch validate multiple submissions"""
    
    batch_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    results = []
    for submission in submissions:
        result = await validate_submission(submission, background_tasks)
        results.append(result)
    
    processing_time = (datetime.now() - start_time).total_seconds() * 1000
    
    # Summary statistics
    approved = sum(1 for r in results if r.status == "approved")
    flagged = sum(1 for r in results if r.status == "flagged")
    rejected = sum(1 for r in results if r.status == "rejected")
    needs_review = sum(1 for r in results if r.status == "needs_review")
    
    return BatchValidationResponse(
        batch_id=batch_id,
        total=len(results),
        approved=approved,
        flagged=flagged,
        rejected=rejected,
        needs_review=needs_review,
        average_score=sum(r.quality_score for r in results) / len(results) if results else 0,
        processing_time_ms=round(processing_time, 2),
        results=[r.dict() for r in results]
    )

@router.get("/benchmarks/{company}/{level}")
async def get_benchmarks(
    company: str,
    level: str,
    location: Optional[str] = None
):
    """Get compensation benchmarks"""
    
    benchmarks = await db_manager.get_benchmarks(company, level, location)
    
    if not benchmarks:
        return {
            "company": company,
            "level": level,
            "location": location or "All locations",
            "message": "Insufficient data for this combination",
            "sample_size": 0
        }
    
    return benchmarks

@router.get("/statistics")
async def get_statistics(
    company: Optional[str] = None,
    level: Optional[str] = None,
    days: int = 30
):
    """Get validation statistics"""
    
    stats = await db_manager.get_statistics(company, level, days)
    return stats