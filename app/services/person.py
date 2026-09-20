from fastapi import HTTPException, status

from app.domain.person import Person
from app.repositories.person import PersonRepository
from app.schemas.person import PersonCreate, PersonUpdate


class PersonService:
    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    async def get_by_id(self, person_id: int) -> Person:
        person = await self._repository.get_by_id(person_id)
        if person is None:
            raise self._not_found(person_id)
        return person

    async def get_all(self) -> list[Person]:
        return await self._repository.get_all()

    async def create(self, payload: PersonCreate) -> Person:
        return await self._repository.create(
            Person(id=None, **payload.model_dump())
        )

    async def update(self, person_id: int, payload: PersonUpdate) -> Person:
        changes = payload.model_dump(exclude_unset=True)
        person = await self._repository.update(person_id, changes)
        if person is None:
            raise self._not_found(person_id)
        return person

    async def delete(self, person_id: int) -> None:
        deleted = await self._repository.delete(person_id)
        if not deleted:
            raise self._not_found(person_id)

    @staticmethod
    def _not_found(person_id: int) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id={person_id} was not found",
        )

