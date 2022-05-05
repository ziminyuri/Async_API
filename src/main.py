import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import film, genre, person
from core import config
from core.logger import LOGGING
from db import elastic, redis
from grpc_client import client
from grpc_client.stubs import auth_pb2_grpc

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await redis.RedisCache.connect(f'{config.REDIS_HOST}:{config.REDIS_PORT}')
    elastic.es = elastic.ElasticSearch(f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}')
    client.stub = auth_pb2_grpc.AuthStub(client.channel)


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()
    client.channel.close()


app.include_router(film.router, prefix='/api/v1/films', tags=['film'])
app.include_router(person.router, prefix='/api/v1/persons', tags=['person'])
app.include_router(genre.router, prefix='/api/v1/genres', tags=['genre'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
