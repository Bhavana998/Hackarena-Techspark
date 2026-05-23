import pytest
from core.validators.vesting_validator import VestingValidator
from core.validators.currency_validator import CurrencyValidator

def test_vesting_validator():
    """Test vesting schedule validation"""
    validator = VestingValidator()
    
    # Valid schedule
    valid_schedule = [
        {"percent": 25, "occurrences": 1},
        {"percent": 25, "occurrences": 4},
        {"percent": 25, "occurrences": 4},
        {"percent": 25, "occurrences": 4}
    ]
    
    result = validator.validate(valid_schedule, 50000)
    assert result['is_valid'] == True
    
    # Invalid schedule (total not 100)
    invalid_schedule = [
        {"percent": 30, "occurrences": 1},
        {"percent": 30, "occurrences": 4},
        {"percent": 30, "occurrences": 4}
    ]
    
    result = validator.validate(invalid_schedule, 50000)
    assert result['is_valid'] == False
    assert len(result['issues']) > 0

def test_currency_validator():
    """Test currency validation"""
    validator = CurrencyValidator()
    
    submission = {
        "baseSalaryCurrency": "INR",
        "stockGrantCurrency": "USD",
        "bonusCurrency": "INR"
    }
    
    result = validator.validate_currency_consistency(submission)
    assert result['has_mixed_currencies'] == True
    assert len(result['issues']) > 0