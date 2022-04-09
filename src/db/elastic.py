from typing import Optional

from elasticsearch import AsyncElasticsearch

from helpers import backoff
from services.es_parser import PARAMS_TYPE, make_query_body

from .base import AbstractRepository


class ElasticSearch(AbstractRepository):
    """Реализация соединения с Elasticsearch"""

    def __init__(self, url: str):
        self.elastic = AsyncElasticsearch(url)

    @backoff()
    async def get(self, index: str, id_: str):
        return await self.elastic.get(index=index, id=id_)

    async def search(self, index: str, params: PARAMS_TYPE):
        query_body = make_query_body(params)
        doc = await self._search(body=query_body, index=index)
        return self.parse_es_response(doc)

    def close(self):
        self.elastic.close()

    @staticmethod
    def parse_es_response(data):
        return [record['_source'] for record in data['hits']['hits']]

    @backoff()
    async def _search(self, index: str, body: dict):
        return await self.elastic.search(body=body, index=index)


es: Optional[ElasticSearch] = None


async def get_elastic() -> ElasticSearch:
    return es
