from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean, JSON, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
from typing import List, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class CompensationSubmission(Base):
    __tablename__ = 'compensation_submissions'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Basic info
    company = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    level = Column(String(20), nullable=False)
    location = Column(String(100), nullable=False)
    years_experience = Column(Integer)
    
    # Compensation
    base_salary = Column(Float, nullable=False)
    base_currency = Column(String(3), default='INR')
    total_compensation = Column(Float)
    stock_value = Column(Float)
    bonus_value = Column(Float)
    
    # Validation results
    quality_score = Column(Float)
    validation_status = Column(String(20))
    anomaly_score = Column(Float)
    confidence_score = Column(Float)
    
    # Metadata
    user_ip = Column(String(45))
    user_agent = Column(String(200))
    
    # Audit
    validation_details = Column(JSON)
    processing_time_ms = Column(Integer)
    
    __table_args__ = (
        Index('idx_company_level', 'company', 'level'),
        Index('idx_created_at', 'created_at'),
        Index('idx_quality_score', 'quality_score'),
        Index('idx_status', 'validation_status'),
    )

class BenchmarkData(Base):
    __tablename__ = 'benchmark_data'
    
    id = Column(Integer, primary_key=True)
    company = Column(String(100), nullable=False)
    level = Column(String(20), nullable=False)
    location = Column(String(100))
    
    p10 = Column(Float)
    p25 = Column(Float)
    p50 = Column(Float)
    p75 = Column(Float)
    p90 = Column(Float)
    mean = Column(Float)
    std_dev = Column(Float)
    sample_size = Column(Integer)
    
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_benchmark_lookup', 'company', 'level', 'location'),
    )

class DatabaseManager:
    def __init__(self, connection_string: str = "sqlite:///levels.db"):
        self.connection_string = connection_string
        self.engine = None
        self.SessionLocal = None
    
    async def initialize(self):
        """Initialize database connection"""
        try:
            self.engine = create_engine(self.connection_string, echo=False)
            Base.metadata.create_all(self.engine)
            self.SessionLocal = sessionmaker(bind=self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
    
    async def health_check(self) -> bool:
        """Check database health"""
        try:
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
        return False
    
    async def save_submission(self, submission_id: str, submission: Dict, validation_result: Dict, client_ip: str = None):
        """Save submission to database"""
        if not self.SessionLocal:
            await self.initialize()
        
        session = self.SessionLocal()
        try:
            submission_obj = CompensationSubmission(
                id=submission_id,
                company=submission.get('company'),
                title=submission.get('title'),
                level=submission.get('level'),
                location=submission.get('location'),
                years_experience=submission.get('yearsOfExperience'),
                base_salary=submission.get('baseSalary'),
                base_currency=submission.get('baseSalaryCurrency', 'INR'),
                total_compensation=submission.get('totalCompensation'),
                stock_value=submission.get('avgAnnualStockGrantValue'),
                bonus_value=submission.get('avgAnnualBonusValue'),
                quality_score=validation_result.get('quality_score'),
                validation_status=validation_result.get('status'),
                anomaly_score=validation_result.get('anomaly_score'),
                confidence_score=validation_result.get('confidence_score'),
                user_ip=client_ip,
                validation_details=validation_result,
                processing_time_ms=validation_result.get('processing_time_ms')
            )
            session.add(submission_obj)
            session.commit()
            logger.info(f"Saved submission {submission_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save submission: {e}")
            raise
        finally:
            session.close()
    
    async def get_historical_submissions(self, limit: int = 10000) -> List[Dict]:
        """Get historical submissions for training"""
        if not self.SessionLocal:
            await self.initialize()
        
        session = self.SessionLocal()
        try:
            submissions = session.query(CompensationSubmission).filter(
                CompensationSubmission.validation_status == 'approved',
                CompensationSubmission.quality_score > 70
            ).limit(limit).all()
            
            return [{
                'baseSalary': s.base_salary,
                'totalCompensation': s.total_compensation,
                'level': s.level,
                'company': s.company,
                'location': s.location,
                'yearsOfExperience': s.years_experience,
                'avgAnnualStockGrantValue': s.stock_value or 0,
                'avgAnnualBonusValue': s.bonus_value or 0
            } for s in submissions]
        finally:
            session.close()
    
    async def get_benchmarks(self, company: str, level: str, location: Optional[str] = None) -> Dict:
        """Get benchmarks from database"""
        if not self.SessionLocal:
            await self.initialize()
        
        session = self.SessionLocal()
        try:
            query = session.query(BenchmarkData).filter(
                BenchmarkData.company == company,
                BenchmarkData.level == level
            )
            if location:
                query = query.filter(BenchmarkData.location == location)
            
            benchmark = query.first()
            if benchmark:
                return {
                    'p10': benchmark.p10,
                    'p25': benchmark.p25,
                    'p50': benchmark.p50,
                    'p75': benchmark.p75,
                    'p90': benchmark.p90,
                    'mean': benchmark.mean,
                    'std_dev': benchmark.std_dev,
                    'sample_size': benchmark.sample_size,
                    'last_updated': benchmark.last_updated
                }
            return {}
        finally:
            session.close()
    
    async def get_statistics(self, company: Optional[str] = None, level: Optional[str] = None, days: int = 30) -> Dict:
        """Get validation statistics"""
        if not self.SessionLocal:
            await self.initialize()
        
        session = self.SessionLocal()
        try:
            from sqlalchemy import func
            query = session.query(CompensationSubmission).filter(
                CompensationSubmission.created_at >= datetime.utcnow() - timedelta(days=days)
            )
            
            if company:
                query = query.filter(CompensationSubmission.company == company)
            if level:
                query = query.filter(CompensationSubmission.level == level)
            
            submissions = query.all()
            
            return {
                'total': len(submissions),
                'avg_score': sum(s.quality_score for s in submissions) / len(submissions) if submissions else 0,
                'approved_count': sum(1 for s in submissions if s.validation_status == 'approved'),
                'flagged_count': sum(1 for s in submissions if s.validation_status == 'flagged'),
                'rejected_count': sum(1 for s in submissions if s.validation_status == 'rejected'),
                'avg_processing_time': sum(s.processing_time_ms for s in submissions) / len(submissions) if submissions else 0
            }
        finally:
            session.close()