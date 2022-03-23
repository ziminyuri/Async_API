from typing import Optional, Union

import orjson
from fastapi import Request
from pydantic import BaseModel
from pydantic.types import PositiveInt


class Page(BaseModel):
    size: PositiveInt = 50
    number: PositiveInt = 1


class BodyQuery(BaseModel):
    page: Optional[Page]
    query: Optional[str]


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def get_params(request: Request) -> dict[str, Union[str, dict]]:
    params: dict[str, Union[str, dict]] = {}
    for key, value in request.query_params.items():
        nested_key = key.removesuffix("]").split("[")
        if len(nested_key) == 2:
            params.setdefault(nested_key[0], {}).update({nested_key[1]: value})
            continue
        params[key] = value

    return params


def make_query_body(params):
    body_params = BodyQuery(**params)
    body = {}

    if body_params.page:
        body['from'] = body_params.page.size * (body_params.page.number - 1)
        body['size'] = body_params.page.size

    if body_params.query:
        body['query'] = {"query_string": {"query": body_params.query}}

    return body
