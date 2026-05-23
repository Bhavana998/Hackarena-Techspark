import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_validate_submission():
    """Test submission validation"""
    submission = {
        "company": "ServiceNow",
        "title": "Software Engineer",
        "jobFamily": "Software Engineer",
        "jobFamilySlug": "software-engineer",
        "level": "IC1",
        "yearsOfExperience": 1,
        "yearsAtCompany": 0,
        "offerDate": "2024-09-09T09:15:00Z",
        "location": "Pune, MH, India",
        "locationSlug": "pune-ind",
        "workArrangement": "hybrid",
        "compPerspective": "offer",
        "exchangeRate": 83.94,
        "baseSalary": 19000,
        "baseSalaryCurrency": "INR",
        "totalCompensation": 27600,
        "firstYearTotalCompensation": 30100,
        "avgAnnualStockGrantValue": 5000,
        "firstYearStockGrantValue": 5000,
        "totalStockGrantValue": 20000,
        "stockGrantCurrency": "USD",
        "avgAnnualBonusValue": 3500,
        "firstYearBonusValue": 6100,
        "bonusCurrency": "INR",
        "vestingSchedule": [],
        "userCurrency": "USD"
    }
    
    response = client.post("/api/v1/validate", json=submission)
    assert response.status_code == 200
    data = response.json()
    assert "quality_score" in data
    assert "status" in data

def test_batch_validation():
    """Test batch validation"""
    submissions = [
        {
            "company": "ServiceNow",
            "title": "Software Engineer",
            "jobFamily": "Software Engineer",
            "jobFamilySlug": "software-engineer",
            "level": "IC1",
            "yearsOfExperience": 1,
            "yearsAtCompany": 0,
            "offerDate": "2024-09-09T09:15:00Z",
            "location": "Pune, MH, India",
            "locationSlug": "pune-ind",
            "workArrangement": "hybrid",
            "compPerspective": "offer",
            "exchangeRate": 83.94,
            "baseSalary": 19000,
            "baseSalaryCurrency": "INR",
            "totalCompensation": 27600,
            "firstYearTotalCompensation": 30100,
            "avgAnnualStockGrantValue": 5000,
            "firstYearStockGrantValue": 5000,
            "totalStockGrantValue": 20000,
            "stockGrantCurrency": "USD",
            "avgAnnualBonusValue": 3500,
            "firstYearBonusValue": 6100,
            "bonusCurrency": "INR",
            "vestingSchedule": [],
            "userCurrency": "USD"
        }
    ]
    
    response = client.post("/api/v1/validate/batch", json=submissions)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "results" in data