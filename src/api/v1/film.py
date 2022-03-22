from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.serializers import FilmDetail, Films
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDetail)
async def get_film_details(film_id: str,
                           film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmDetail(**film.dict())


@router.get('/search/', response_model=Films)
async def film_search(query: str, page: int = 1, size: int = 50,
                      film_service: FilmService = Depends(get_film_service)) -> Films:
    films = await film_service.get_by_query(query, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return Films.parse_obj(films.__root__)


@router.get('', response_model=Films)
async def get_films(sort: str = None, genre: str = None, page: int = 1, size: int = 50,
                    film_service: FilmService = Depends(get_film_service)) -> Films:
    films = await film_service.get_films(sort, genre, page, size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return Films.parse_obj(films.__root__)
