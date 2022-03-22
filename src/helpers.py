from typing import Union

import orjson
from fastapi import Request


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def get_params(request: Request) -> dict[str, Union[str, dict]]:
    params: dict[str, Union[str, dict]] = {}
    for key, value in request.query_params.items():
        nested_key = key.removesuffix("]").split("[")
        if len(nested_key) == 2:
            params.setdefault(nested_key[0], {}).update({nested_key[1]: value})  # type: ignore
            continue
        params[key] = value

    return params
