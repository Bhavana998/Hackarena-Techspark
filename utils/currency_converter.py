from typing import Dict, Optional
import aiohttp
from datetime import datetime, timedelta

class CurrencyConverter:
    """Currency conversion utility"""
    
    def __init__(self):
        self.rates: Dict[str, float] = {
            'USD': 1.0,
            'INR': 83.94,
            'EUR': 0.92,
            'GBP': 0.79,
            'CAD': 1.35,
            'AUD': 1.51
        }
        self.last_update = None
    
    async def fetch_rates(self):
        """Fetch latest exchange rates"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.exchangerate-api.com/v4/latest/USD") as resp:
                    data = await resp.json()
                    self.rates = data.get('rates', self.rates)
                    self.last_update = datetime.now()
        except Exception:
            pass
    
    async def convert(self, amount: float, from_currency: str, to_currency: str = 'USD') -> float:
        """Convert currency"""
        if from_currency == to_currency:
            return amount
        
        # Refresh rates if needed
        if not self.last_update or datetime.now() - self.last_update > timedelta(hours=1):
            await self.fetch_rates()
        
        # Convert to USD first
        usd_amount = amount / self.rates.get(from_currency, 1.0)
        
        # Convert to target currency
        return usd_amount * self.rates.get(to_currency, 1.0)