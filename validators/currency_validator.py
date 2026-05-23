from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class CurrencyValidator:
    """Handle multi-currency validation"""
    
    def __init__(self):
        self.exchange_rates = {
            'USD': 1.0,
            'INR': 83.94,
            'EUR': 0.92,
            'GBP': 0.79,
        }
    
    def validate_currency_consistency(self, submission: Dict) -> Dict[str, Any]:
        """Check currency consistency across fields"""
        
        issues = []
        
        base_currency = submission.get('baseSalaryCurrency', 'INR')
        stock_currency = submission.get('stockGrantCurrency', 'USD')
        bonus_currency = submission.get('bonusCurrency', 'INR')
        
        # Check if mixed currencies exist
        currencies = set([base_currency, stock_currency, bonus_currency])
        if len(currencies) > 1:
            issues.append({
                'type': 'mixed_currencies',
                'severity': 'medium',
                'message': f"Mixed currencies detected: Base({base_currency}), Stock({stock_currency}), Bonus({bonus_currency})"
            })
        
        return {
            'has_mixed_currencies': len(currencies) > 1,
            'issues': issues,
            'currencies': {
                'base': base_currency,
                'stock': stock_currency,
                'bonus': bonus_currency
            }
        }
    
    def convert_currency(self, value: float, from_currency: str, to_currency: str = 'USD') -> float:
        """Convert currency using exchange rates"""
        if from_currency == to_currency:
            return value
        
        rate = self.exchange_rates.get(from_currency, 1.0) / self.exchange_rates.get(to_currency, 1.0)
        return value * rate