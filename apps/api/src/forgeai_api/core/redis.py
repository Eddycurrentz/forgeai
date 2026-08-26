from redis.asyncio import Redis

from forgeai_api.core.config import Settings


def create_redis_client(settings: Settings) -> Redis:
    return Redis.from_url(settings.redis_url_str(), decode_responses=True)


async def ping_redis(client: Redis) -> bool:
    return bool(await client.ping())
