import json

from redis.asyncio import Redis as AsyncRedis

from src.application.interfaces import ITokenRepository


class RedisTokenRepository(ITokenRepository):
    def __init__(self, redis_client: AsyncRedis):
        self.redis = redis_client

    def _make_key(self, user_id: str, jti: str) -> str:
        return f"refresh_token:{user_id}:{jti}"

    def _make_access_key_for_blacklist(self, access_jti: str) -> str:
        return f"blacklist:access_token:{access_jti}"

    async def save(self, payload: dict, ttl_seconds: int) -> None:
        key = self._make_key(payload.get("sub"), payload.get("jti"))
        print(f"-------------Save refresh token for {key}")
        data = {
            "user_id": payload.get("sub"),
            "jti": payload.get("jti"),
            "created_at": payload.get("iat"),
            "expires_at": payload.get("exp"),
        }
        await self.redis.setex(key, ttl_seconds, json.dumps(data))

    async def exists(self, user_id: str, jti: str) -> bool:
        key = self._make_key(user_id, jti)
        return bool(await self.redis.exists(key))

    async def delete(self, user_id: str, jti: str) -> None:
        key = self._make_key(user_id, jti)
        await self.redis.delete(key)

    async def delete_all_for_user(self, user_id: str) -> None:
        pattern = f"refresh_token:{user_id}:*"
        cursor = 0
        while True:
            cursor, keys = await self.redis.scan(cursor=cursor, match=pattern, count=100)
            if keys:
                await self.redis.delete(*keys)
            if cursor == 0:
                break

    async def count_for_user(self, user_id: str) -> int:
        pattern = f"refresh_token:{user_id}:*"
        keys = []
        cursor = 0
        while True:
            cursor, batch = await self.redis.scan(cursor=cursor, match=pattern, count=100)
            keys.extend(batch)
            if cursor == 0:
                break
        return len(keys)

    async def save_access_token_in_blacklist(self, access_jti: str, ttl_seconds: int) -> None:
        key = self._make_access_key_for_blacklist(access_jti)
        print(f"-------------Save access token for {key}")
        await self.redis.setex(f"{key}", ttl_seconds, "1")

    async def exists_access_token_in_blacklist(self, access_jti: str) -> bool:
        key = self._make_access_key_for_blacklist(access_jti)
        return bool(await self.redis.exists(key))
