def film_search_query(query):
    return {
        "bool": {
            "should": [{
                "match": {
                    "title": query
                },
                "match": {
                    "description": query
                }
            }]
        }}
