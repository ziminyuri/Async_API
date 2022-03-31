from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.query_params import BaseParams
from models.genre import Genre, Genres
from services.genre import GenreService, get_genre_service
from dictionary import errors_dict

router = APIRouter()


@router.get(
    '',
    response_model=Genres,
    summary='List of genres',
)
async def genres_list(
        params: BaseParams = Depends(),
        genres_service: GenreService = Depends(get_genre_service)
) -> Genres:

    genre_list = await genres_service.get_by_params(params)
    if not genre_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors_dict['404_genres'])
    return Genres.parse_obj(genre_list.__root__)


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:

    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=errors_dict['404_genre'])

    return Genre(**genre.dict())
