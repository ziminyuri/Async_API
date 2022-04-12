import logging
import os

import backoff
from aioredis import ConnectionError, Redis

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

r = Redis(host=REDIS_HOST, port=REDIS_PORT)

logger = logging.getLogger()


@backoff.on_exception(backoff.expo, ConnectionError, max_tries=20)
def check_redis():
    if not r.ping():
        logger.info('Redis not connected, retry')
        raise ConnectionError
    else:
        logger.info('Redis connected.')


if __name__ == '__main__':
    check_redis()
