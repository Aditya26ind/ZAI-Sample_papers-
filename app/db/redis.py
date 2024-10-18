# app/db/redis.py
import redis.asyncio as aioredis

class RedisDB:
    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis = aioredis.from_url(redis_url)

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value):
        await self.redis.set(key, value)

# Automatically connect to Redis service defined in docker-compose.yml
redisdb = RedisDB()