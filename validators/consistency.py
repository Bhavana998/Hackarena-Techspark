from typing import Dict, List, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConsistencyValidator:
    """Validate internal consistency of submissions"""
    
    def validate(self, submission: Dict) -> Dict[str, Any]:
        """Check internal consistency"""
        
        issues = []
        
        # Check if total compensation matches components
        base = submission.get('baseSalary', 0)
        bonus = submission.get('avgAnnualBonusValue', 0)
        stock = submission.get('avgAnnualStockGrantValue', 0)
        
        calculated_total = base + bonus + (stock * submission.get('exchangeRate', 83.94))
        reported_total = submission.get('totalCompensation', 0)
        
        if reported_total > 0:
            diff_percent = abs(calculated_total - reported_total) / reported_total * 100
            if diff_percent > 10:
                issues.append({
                    'type': 'inconsistent_total',
                    'severity': 'high',
                    'message': f"Total compensation mismatch: reported {reported_total:,.0f} vs calculated {calculated_total:,.0f}"
                })
        
        # Check years of experience
        years_exp = submission.get('yearsOfExperience', 0)
        years_at_company = submission.get('yearsAtCompany', 0)
        
        if years_at_company > years_exp:
            issues.append({
                'type': 'experience_mismatch',
                'severity': 'high',
                'message': f"Years at company ({years_at_company}) exceeds total experience ({years_exp})"
            })
        
        # Check for negative values
        for field in ['baseSalary', 'avgAnnualBonusValue', 'avgAnnualStockGrantValue']:
            value = submission.get(field, 0)
            if value < 0:
                issues.append({
                    'type': 'negative_value',
                    'severity': 'critical',
                    'message': f"{field} cannot be negative"
                })
        
        return {
            'is_consistent': len(issues) == 0,
            'issues': issues,
            'calculated_total': calculated_total,
            'reported_total': reported_total
        }