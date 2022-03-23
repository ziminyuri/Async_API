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


def films_query(genre=None):
    if genre:
        return {
            "nested": {
                "path": "genres",
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"genres.id": genre}}
                        ]
                    }
                }
            }
        }
    return {
        "match_all": {}
    }
