def make_query_body(params) -> dict:
    body = {}

    if params.page:
        body['from'] = params.size * (params.page - 1)
        body['size'] = params.size

    if params.query:
        body['query'] = {"query_string": {"query": params.query}}

    if params.sort:
        field = params.sort.removeprefix("-")
        direction = "desc" if params.sort.startswith("-") else "asc"
        body["sort"] = {field: {"order": direction}}

    return body
