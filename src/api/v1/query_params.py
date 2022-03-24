from fastapi import Query


class BaseParams:
    def __init__(
            self,
            query: str = Query(None, description="Поиск по названию"),
            sort: str = Query(None, description="Сортировка"),
            page: int = Query(1, description="Номер страницы"),
            size: int = Query(50, description='Количество элементов на странице')
    ):
        self.sort = sort
        self.size = size
        self.page = page
        self.query = query


class FilmSearchParams:
    def __init__(
            self,
            query: str = Query(..., description="Поиск по названию и описание"),
            page: int = Query(1, description="Номер страницы"),
            size: int = Query(50, description='Количество элементов на странице')
    ):
        self.size = size
        self.page = page
        self.query = query


class FilmsParams:
    def __init__(
            self,
            sort: str = Query(None, description="Сортировка"),
            genre: str = Query(None, description="Фильтрация по жанру"),
            page: int = Query(1, description="Номер страницы"),
            size: int = Query(50, description='Количество элементов на странице')
    ):
        self.genre = genre
        self.sort = sort
        self.size = size
        self.page = page
