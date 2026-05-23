"""Simple test to verify the API works"""

import requests
import json

# Test data
test_submission = {
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
    "vestingSchedule": [
        {"percent": 25, "occurrences": 1},
        {"percent": 25, "occurrences": 4},
        {"percent": 25, "occurrences": 4},
        {"percent": 25, "occurrences": 4}
    ],
    "userCurrency": "USD"
}

print("Testing API at http://localhost:8000...")

try:
    # Test health endpoint
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Health check: {response.status_code}")
    
    # Test validation
    response = requests.post(
        "http://localhost:8000/api/v1/validate",
        json=test_submission,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Validation successful!")
        print(f"   Quality Score: {result.get('quality_score')}/100")
        print(f"   Status: {result.get('status')}")
        print(f"   Confidence: {result.get('confidence_level')*100:.1f}%")
        print(f"   Processing Time: {result.get('processing_time_ms')}ms")
    else:
        print(f"❌ Validation failed: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to API. Make sure it's running:")
    print("   python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
except Exception as e:
    print(f"❌ Error: {e}")