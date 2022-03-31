from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.query_params import FilmSearchParams, FilmsParams
from serializers.film import FilmDetail, Films
from services.film import FilmService, get_film_service
from dictionary import errors_dict

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDetail)
async def get_film_details(film_id: str,
                           film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors_dict['404_film'])

    return FilmDetail(**film.dict())


@router.get('/search/', response_model=Films)
async def film_search(params: FilmSearchParams = Depends(),
                      film_service: FilmService = Depends(get_film_service)) -> Films:
    films = await film_service.get_by_params(params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors_dict['404_films'])

    return Films.parse_obj(films.__root__)


@router.get('', response_model=Films)
async def get_films(params: FilmsParams = Depends(),
                    film_service: FilmService = Depends(get_film_service)) -> Films:
    films = await film_service.get_by_params(params)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors_dict['404_films'])

    return Films.parse_obj(films.__root__)
