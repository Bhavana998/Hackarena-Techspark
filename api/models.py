from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class VestingScheduleItem(BaseModel):
    percent: float = Field(..., ge=0, le=100)
    occurrences: int = Field(..., ge=1, le=48)

class AdditionalBonus(BaseModel):
    type: str
    value: float
    currency: str = "INR"

class CompanyInfo(BaseModel):
    registered: bool = True
    icon: str = ""
    name: str
    slug: str

class CompensationSubmission(BaseModel):
    uuid: Optional[str] = None
    company: str
    title: str
    jobFamily: str = "Software Engineer"
    jobFamilySlug: str = "software-engineer"
    level: str = "IC1"
    focusTag: Optional[str] = None
    yearsOfExperience: int = 0
    yearsAtCompany: int = 0
    yearsAtLevel: Optional[int] = None
    offerDate: str = ""
    location: str
    locationSlug: str = ""
    workArrangement: str = "hybrid"
    compPerspective: str = "offer"
    cityId: Optional[int] = None
    dmaId: Optional[int] = None
    countryId: Optional[int] = None
    exchangeRate: float = 83.94
    baseSalary: float
    baseSalaryCurrency: str = "INR"
    totalCompensation: float
    firstYearTotalCompensation: float
    avgAnnualStockGrantValue: float = 0
    firstYearStockGrantValue: float = 0
    totalStockGrantValue: float = 0
    stockGrantCurrency: str = "USD"
    avgAnnualBonusValue: float = 0
    firstYearBonusValue: float = 0
    bonusCurrency: str = "INR"
    vestingSchedule: Optional[List[VestingScheduleItem]] = []
    additionalBonuses: Optional[List[AdditionalBonus]] = []
    userCurrency: str = "USD"
    companyInfo: Optional[CompanyInfo] = None

class ValidationResponse(BaseModel):
    submission_id: str
    timestamp: datetime
    quality_score: float
    confidence_level: float
    status: str
    anomaly_detection: Dict[str, Any]
    currency_validation: Dict[str, Any]
    vesting_validation: Dict[str, Any]
    geographic_validation: Optional[Dict[str, Any]] = None
    recommendations: List[str]
    processing_time_ms: float

class BatchValidationResponse(BaseModel):
    batch_id: str
    total: int
    approved: int
    flagged: int
    rejected: int
    needs_review: int
    average_score: float
    processing_time_ms: float
    results: List[Dict[str, Any]]