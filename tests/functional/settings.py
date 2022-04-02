from pydantic import BaseSettings, Field

SERVICE_URL = 'http://127.0.0.1:8000'
API_VERSION = '/api/v1/'


class TestSettings(BaseSettings):
    """Настройки для тестов"""
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    redis_host: str = Field('redis://localhost', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
