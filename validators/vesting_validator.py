from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class VestingValidator:
    """Validate stock vesting schedules"""
    
    def validate(self, vesting_schedule: List[Dict], stock_value: float) -> Dict[str, Any]:
        """Validate vesting schedule logic"""
        
        issues = []
        
        if not vesting_schedule:
            return {
                'is_valid': True,
                'issues': [],
                'suggestion': None
            }
        
        # Check total percentage
        total_percent = sum(v.get('percent', 0) for v in vesting_schedule)
        if abs(total_percent - 100) > 0.01:
            issues.append({
                'type': 'invalid_total',
                'severity': 'critical',
                'message': f"Vesting total is {total_percent}%, must be 100%"
            })
        
        # Check for cliff periods
        if len(vesting_schedule) > 0:
            first_year = vesting_schedule[0]
            if first_year.get('percent', 0) > 25:
                issues.append({
                    'type': 'large_cliff',
                    'severity': 'medium',
                    'message': f"First year cliff of {first_year['percent']}% is unusually high"
                })
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'total_percent': total_percent,
            'suggestion': self._generate_suggestion(vesting_schedule) if issues else None
        }
    
    def _generate_suggestion(self, vesting_schedule: List[Dict]) -> str:
        """Generate suggested fix"""
        total = sum(v.get('percent', 0) for v in vesting_schedule)
        if total != 100:
            return f"Adjust percentages to sum to 100% (currently {total}%)"
        return None