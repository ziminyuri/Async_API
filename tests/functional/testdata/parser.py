def filter_films_by_genre(films: list, id: int) -> list:
    sorted_films = []
    for film in films:
        genres = film['_source']['genres']
        for genre in genres:
            if genre['id'] == id:
                sorted_films.append(film)
                break

    return sorted_films


def filter_by_field(films: list, field: str, value: str) -> list:
    sorted_films = []
    for film in films:
        if isinstance(film['_source'][field], str):
            if film['_source'][field].find(value) != -1:
                sorted_films.append(film)

    return sorted_films


def paginate(objs: list, page: int, size: int) -> list:
    offset = (page - 1) * size
    return objs[offset:offset+size]
