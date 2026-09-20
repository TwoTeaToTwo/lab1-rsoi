from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app.api.dependencies import PersonServiceDependency
from app.schemas.person import PersonCreate, PersonResponse, PersonUpdate


router = APIRouter(prefix="/persons", tags=["Persons"])


@router.get("", response_model=list[PersonResponse])
async def get_persons(service: PersonServiceDependency) -> list[PersonResponse]:
    persons = await service.get_all()
    return [PersonResponse.model_validate(person) for person in persons]


@router.get("/{personId}", response_model=PersonResponse)
async def get_person(
    person_id: Annotated[int, Path(alias="personId", ge=1)],
    service: PersonServiceDependency,
) -> PersonResponse:
    person = await service.get_by_id(person_id)
    return PersonResponse.model_validate(person)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_person(
    payload: PersonCreate,
    service: PersonServiceDependency,
) -> Response:
    person = await service.create(payload)
    # The task contract requires a relative URI in Location.
    # А он сам не умеет получать текущую локацию для метода ручки?
    # А то это захардкоженная строка, может потом принести проблем
    location = f"/api/v1/persons/{person.id}"
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": location},
    )


@router.patch("/{personId}", response_model=PersonResponse)
async def update_person(
    person_id: Annotated[int, Path(alias="personId", ge=1)],
    payload: PersonUpdate,
    service: PersonServiceDependency,
) -> PersonResponse:
    person = await service.update(person_id, payload)
    return PersonResponse.model_validate(person)


@router.delete("/{personId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    person_id: Annotated[int, Path(alias="personId", ge=1)],
    service: PersonServiceDependency,
) -> Response:
    await service.delete(person_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
