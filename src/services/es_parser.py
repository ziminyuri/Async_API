from typing import Optional, Union

from api.v1.query_params import BaseParams, FilmSearchParams, FilmsParams

PARAMS_TYPE = Union[BaseParams, FilmSearchParams, FilmsParams]


def make_query_body(params: Optional[PARAMS_TYPE]) -> dict:
    body = {}

    if params.page:
        body['from'] = params.size * (params.page - 1)
        body['size'] = params.size

    body = _get_genre(body, params)
    body = _get_query(body, params)
    body = _get_sort(body, params)

    return body


def _get_sort(body: dict, params: Optional[PARAMS_TYPE]) -> dict:
    if params is BaseParams:
        if params.sort:
            field = params.sort.removeprefix("-")
            direction = "desc" if params.sort.startswith("-") else "asc"
            body["sort"] = {field: {"order": direction}}
    return body


def _get_query(body: dict, params: Optional[PARAMS_TYPE]) -> dict:
    """ Получение поискового запроса """
    if params is BaseParams:
        if params.query:
            body['query'] = {"query_string": {"query": params.query}}

    elif params is FilmSearchParams:
        if params.query:
            body['query'] = {
                "bool": {
                    "should": [{
                        "match": {
                            "title": params.query
                        },
                        "match": {
                            "description": params.query
                        }
                    }]
                }}
    return body


def _get_genre(body: dict, params: Optional[PARAMS_TYPE]) -> dict:
    """ Соритровака по жанрам для фильмов"""

    if params is FilmsParams:
        if params.genre:
            body['query'] = {
                "nested": {
                    "path": "genres",
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"genres.id": params.genre}}
                            ]
                        }
                    }
                }
            }

    return body
