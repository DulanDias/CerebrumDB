import aioredis
import os
import hashlib

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

class Cache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(REDIS_URL)

    def generate_key(self, base_key, filters=None):
        """
        Generate a unique cache key based on the base key and filters.
        """
        if filters:
            filters_str = str(sorted(filters.items()))
            hash_suffix = hashlib.md5(filters_str.encode()).hexdigest()
            return f"{base_key}:{hash_suffix}"
        return base_key

    async def set(self, key, value, expire=3600, filters=None):
        """
        Set a value in the cache with a unique key based on filters.
        """
        unique_key = self.generate_key(key, filters)
        await self.redis.set(unique_key, value, ex=expire)

    async def get(self, key, filters=None):
        """
        Get a value from the cache using a unique key based on filters.
        """
        unique_key = self.generate_key(key, filters)
        return await self.redis.get(unique_key)

cache = Cache()