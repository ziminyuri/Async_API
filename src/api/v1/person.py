from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.v1.query_params import BaseParams
from models.person import Person, Persons
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    "/search",
    response_model=Persons,
    summary="Search person"
)
@router.get(
    "",
    response_model=Persons,
    summary="List of person",
)
async def persons_list(
        params: BaseParams = Depends(),
        person_service: PersonService = Depends(get_person_service)
) -> Persons:

    person_list = await person_service.get_by_params(params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="PERSON_NOT_FOUND")
    return Persons.parse_obj(person_list.__root__)


@router.get('/{person_id}', response_model=Person)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
        ) -> Person:

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(**person.dict())
