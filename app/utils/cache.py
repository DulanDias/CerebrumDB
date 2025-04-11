import aioredis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

class Cache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(REDIS_URL)

    async def set(self, key, value, expire=3600):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key):
        return await self.redis.get(key)

cache = Cache()