from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from services.person import PersonService, get_person_service
from services.utils import get_params
from models.person import Person

router = APIRouter()


@router.get(
    "",
    response_model=list[Person],
    summary="List of person",
    description="List of persons with full_name, roles and film_ids",
    response_description="List of persons with id",
)
async def persons_list(
    request: Request, person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    params = get_params(request)
    person_list = await person_service.get_by_params(**params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="PERSON_NOT_FOUND")
    return [
        Person(
            id=person.id,
            full_name=person.full_name,
            roles=person.roles,
            films=person.films,
        )
        for person in person_list
    ]


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(**person.dict())