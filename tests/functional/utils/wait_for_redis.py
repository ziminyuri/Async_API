import os
import time

from aioredis import ConnectionError, Redis

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6389))

r = Redis(host=REDIS_HOST, port=REDIS_PORT)

is_connected = False

while not is_connected:
    try:
        is_connected = r.ping()
        print('Redis connected.')
    except ConnectionError:
        print('Redis not connected, retry in 10 seconds...')
        time.sleep(10)
