import aioredis
import json
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis client for caching and rate limiting"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.client = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = await aioredis.from_url(self.redis_url, decode_responses=True)
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None
        
        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None
    
    async def set(self, key: str, value: Any, expire: int = 3600):
        """Set value in cache"""
        if not self.client:
            return
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        await self.client.setex(key, expire, value)
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        if not self.client:
            return 0
        
        return await self.client.incrby(key, amount)
    
    async def get_rate_limit(self, key: str, limit: int = 100, window: int = 60) -> tuple:
        """Check rate limit"""
        if not self.client:
            return (0, False)
        
        current = await self.client.incr(key)
        if current == 1:
            await self.client.expire(key, window)
        
        return (current, current > limit)