import requests
import json

response = requests.post(
    "http://localhost:8000/api/v1/validate",
    json={
        "company": "ServiceNow",
        "title": "Software Engineer", 
        "level": "IC1",
        "location": "Pune, India",
        "baseSalary": 19000,
        "totalCompensation": 27600,
        "yearsOfExperience": 1,
        "avgAnnualStockGrantValue": 5000,
        "avgAnnualBonusValue": 3500
    }
)

print(json.dumps(response.json(), indent=2))