"""
Redis client for caching and session management
"""

import redis.asyncio as redis
from typing import Optional, Any, Dict
import json
import logging
from datetime import timedelta

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    """Redis client wrapper"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("✅ Connected to Redis successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("🔌 Redis connection closed")
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """Set a key-value pair"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = json.dumps(value) if not isinstance(value, str) else value
            result = await self.redis_client.set(key, serialized_value, ex=expire)
            return result
        except Exception as e:
            logger.error(f"Redis SET error: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value by key"""
        if not self.redis_client:
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value is None:
                return None
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Delete a key"""
        if not self.redis_client:
            return False
        
        try:
            result = await self.redis_client.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis_client:
            return False
        
        try:
            result = await self.redis_client.exists(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Redis EXISTS error: {e}")
            return False
    
    async def set_hash(self, key: str, mapping: Dict[str, Any], expire: Optional[int] = None):
        """Set hash fields"""
        if not self.redis_client:
            return False
        
        try:
            # Serialize complex values
            serialized_mapping = {}
            for k, v in mapping.items():
                serialized_mapping[k] = json.dumps(v) if not isinstance(v, str) else v
            
            result = await self.redis_client.hset(key, mapping=serialized_mapping)
            if expire:
                await self.redis_client.expire(key, expire)
            return result
        except Exception as e:
            logger.error(f"Redis HSET error: {e}")
            return False
    
    async def get_hash(self, key: str) -> Optional[Dict[str, Any]]:
        """Get all hash fields"""
        if not self.redis_client:
            return None
        
        try:
            result = await self.redis_client.hgetall(key)
            if not result:
                return None
            
            # Deserialize values
            deserialized_result = {}
            for k, v in result.items():
                try:
                    deserialized_result[k] = json.loads(v)
                except json.JSONDecodeError:
                    deserialized_result[k] = v
            
            return deserialized_result
        except Exception as e:
            logger.error(f"Redis HGETALL error: {e}")
            return None
    
    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a numeric value"""
        if not self.redis_client:
            return None
        
        try:
            result = await self.redis_client.incrby(key, amount)
            return result
        except Exception as e:
            logger.error(f"Redis INCRBY error: {e}")
            return None
    
    async def set_with_ttl(self, key: str, value: Any, ttl_seconds: int):
        """Set key with TTL"""
        return await self.set(key, value, expire=ttl_seconds)
    
    async def get_ttl(self, key: str) -> Optional[int]:
        """Get TTL of a key"""
        if not self.redis_client:
            return None
        
        try:
            result = await self.redis_client.ttl(key)
            return result if result >= 0 else None
        except Exception as e:
            logger.error(f"Redis TTL error: {e}")
            return None
    
    async def health_check(self) -> bool:
        """Check Redis health"""
        try:
            if not self.redis_client:
                return False
            await self.redis_client.ping()
            return True
        except Exception:
            return False

# Global Redis client instance
redis_client = RedisClient()

async def init_redis():
    """Initialize Redis connection"""
    await redis_client.connect()

async def close_redis():
    """Close Redis connection"""
    await redis_client.disconnect()

# Cache decorators and utilities
class CacheManager:
    """Cache management utilities"""
    
    @staticmethod
    def generate_cache_key(prefix: str, *args) -> str:
        """Generate cache key"""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ":".join(key_parts)
    
    @staticmethod
    async def cache_conversation_context(user_id: str, context: Dict[str, Any], ttl: int = 3600):
        """Cache conversation context"""
        key = CacheManager.generate_cache_key("context", user_id)
        await redis_client.set(key, context, expire=ttl)
    
    @staticmethod
    async def get_conversation_context(user_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation context"""
        key = CacheManager.generate_cache_key("context", user_id)
        return await redis_client.get(key)
    
    @staticmethod
    async def cache_user_session(session_id: str, user_data: Dict[str, Any], ttl: int = 86400):
        """Cache user session"""
        key = CacheManager.generate_cache_key("session", session_id)
        await redis_client.set_hash(key, user_data, expire=ttl)
    
    @staticmethod
    async def get_user_session(session_id: str) -> Optional[Dict[str, Any]]:
        """Get user session"""
        key = CacheManager.generate_cache_key("session", session_id)
        return await redis_client.get_hash(key)
    
    @staticmethod
    async def invalidate_user_session(session_id: str):
        """Invalidate user session"""
        key = CacheManager.generate_cache_key("session", session_id)
        await redis_client.delete(key)
    
    @staticmethod
    async def cache_faq_results(query_hash: str, results: list, ttl: int = 1800):
        """Cache FAQ search results"""
        key = CacheManager.generate_cache_key("faq", query_hash)
        await redis_client.set(key, results, expire=ttl)
    
    @staticmethod
    async def get_cached_faq_results(query_hash: str) -> Optional[list]:
        """Get cached FAQ results"""
        key = CacheManager.generate_cache_key("faq", query_hash)
        return await redis_client.get(key)

# Export cache manager instance
cache_manager = CacheManager() 