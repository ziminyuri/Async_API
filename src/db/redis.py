from hashlib import sha256
from typing import Optional

from aioredis import Redis

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis


def get_key_for_list(index, params):
    key = f'{index}:{params}'.encode('utf-8')
    return str(sha256(key).hexdigest())
