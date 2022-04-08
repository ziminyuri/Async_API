import os

from pydantic import BaseSettings, Field

SERVICE_URL = os.getenv('SERVICE_URL', 'http://127.0.0.1:8000')
API_VERSION = '/api/v1/'

REDIS_HOST = os.getenv('REDIS_HOST', 'redis://localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'http://127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))


class TestSettings(BaseSettings):
    """Настройки для тестов"""
    es_host: str = Field(f'{ELASTIC_HOST}:{ELASTIC_PORT}')
    redis_host: str = Field(REDIS_HOST)
    redis_port: int = Field(REDIS_PORT)
