from typing import Dict, Any, List, Optional
import json
import os
import logging

logger = logging.getLogger(__name__)

class GeographicValidator:
    """Validate geographic location data"""
    
    def __init__(self):
        self.location_hubs = {
            'Pune': 'India',
            'Bangalore': 'India',
            'Hyderabad': 'India',
            'Mumbai': 'India',
            'San Francisco': 'USA',
            'New York': 'USA',
            'Seattle': 'USA',
            'Austin': 'USA'
        }
        
        self.cost_multipliers = {
            'India': 0.3,
            'USA': 1.0,
            'UK': 0.9,
            'Canada': 0.85,
            'Germany': 0.8
        }
    
    def validate_location(self, location: str, company: str) -> Dict[str, Any]:
        """Validate location data"""
        
        issues = []
        
        # Extract city from location string
        city = location.split(',')[0].strip() if location else ""
        
        # Check if location exists in our database
        if city not in self.location_hubs:
            issues.append({
                'type': 'unrecognized_location',
                'severity': 'low',
                'message': f"Location '{city}' may need verification"
            })
        
        # Get country
        country = self.location_hubs.get(city, 'Unknown')
        cost_multiplier = self.cost_multipliers.get(country, 0.5)
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'city': city,
            'country': country,
            'cost_multiplier': cost_multiplier,
            'confidence': 0.9 if city in self.location_hubs else 0.5
        }
    
    def get_cost_multiplier(self, location: str) -> float:
        """Get cost of living multiplier for location"""
        city = location.split(',')[0].strip() if location else ""
        country = self.location_hubs.get(city, 'Unknown')
        return self.cost_multipliers.get(country, 0.5)