import os
from logging import config as logging_config

from dotenv import load_dotenv

from core.logger import LOGGING

load_dotenv()

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))

ELASTIC_HOST = os.getenv('ELASTIC_HOST')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT'))

GRPC_HOST = os.getenv('GRPC_HOST')
GRPC_PORT = os.getenv('GRPC_PORT')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
