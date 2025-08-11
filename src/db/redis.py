from redis.asyncio import StrictRedis

from src.config import get_settings


settings = get_settings()

token_blocklist = StrictRedis.from_url(
    url=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)


async def add_jti_to_blocklist(jti: str) -> None:

    await token_blocklist.set(name=jti, value="", ex=settings.JWT_EXPIRY)


async def jti_in_blocklist(jti: str) -> bool:

    return await token_blocklist.get(name=jti) is not None
