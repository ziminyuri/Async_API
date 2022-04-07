from dataclasses import dataclass
from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


async def populate_es(es_client: AsyncElasticsearch,
                      index: str, body: dict, docs: List[str]):
    """Создаем индекс и заполняем базу данных ES"""
    await es_client.indices.create(index=index, body=body)
    await async_bulk(es_client, docs)
    await es_client.indices.refresh(index=index)


async def delete_es_index(es_client: AsyncElasticsearch, index: str = None):
    """Удаляем индекс из ES"""
    await es_client.indices.delete(index=index, ignore=[400, 404])
