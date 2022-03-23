from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from helpers import get_params
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    "/search",
    response_model=list[Genre],
    summary="Search genres"
)
@router.get(
    "",
    response_model=list[Genre],
    summary="List of genres",
)
async def genres_list(
    request: Request, person_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:

    params = get_params(request)
    genre_list = await person_service.get_by_params(**params)
    if not genre_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return [
        Genre(
            id=genre.id,
            name=genre.name,
            films=genre.films,
        )
        for genre in genre_list
    ]


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:

    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(**genre.dict())
