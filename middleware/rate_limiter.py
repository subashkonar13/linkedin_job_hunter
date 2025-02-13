from fastapi import HTTPException
from datetime import datetime, timedelta
import redis
import asyncio

class RateLimiter:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.limits = {
            'linkedin_search': {'calls': 10, 'period': 3600},  # 10 calls per hour
            'linkedin_apply': {'calls': 20, 'period': 86400},  # 20 applications per day
            'openai_calls': {'calls': 50, 'period': 3600}      # 50 calls per hour
        }
    
    async def check_rate_limit(self, key: str, limit_type: str):
        current = int(self.redis.get(key) or 0)
        limit_info = self.limits[limit_type]
        
        if current >= limit_info['calls']:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded for {limit_type}"
            )
            
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, limit_info['period'])
        pipe.execute()
