from typing import List, Union
import numpy as np

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    symbols = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£"
    }
    
    symbol = symbols.get(currency, "$")
    
    if amount >= 1_000_000:
        return f"{symbol}{amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{symbol}{amount/1_000:.1f}K"
    else:
        return f"{symbol}{amount:,.0f}"

def calculate_percentile(data: List[float], percentile: float) -> float:
    """Calculate percentile of data"""
    return np.percentile(data, percentile)

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def mask_ip(ip: str) -> str:
    """Mask IP address for privacy"""
    parts = ip.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.xxx.xxx"
    return ip