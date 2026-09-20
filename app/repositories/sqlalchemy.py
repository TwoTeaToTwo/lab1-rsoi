from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.person import Person
from app.models.person import PersonModel
from app.repositories.person import PersonRepository


class SqlAlchemyPersonRepository(PersonRepository):
    """PostgreSQL-ready repository based on SQLAlchemy 2.x."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(model: PersonModel) -> Person:
        return Person(
            id=model.id,
            name=model.name,
            age=model.age,
            address=model.address,
            work=model.work,
        )

    async def get_by_id(self, person_id: int) -> Person | None:
        model = await self._session.get(PersonModel, person_id)
        return self._to_domain(model) if model is not None else None

    async def get_all(self) -> list[Person]:
        result = await self._session.scalars(
            select(PersonModel).order_by(PersonModel.id)
        )
        return [self._to_domain(model) for model in result]

    async def create(self, person: Person) -> Person:
        model = PersonModel(
            name=person.name,
            age=person.age,
            address=person.address,
            work=person.work,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def update(self, person_id: int, changes: dict[str, Any]) -> Person | None:
        model = await self._session.get(PersonModel, person_id)
        if model is None:
            return None

        for field, value in changes.items():
            setattr(model, field, value)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def delete(self, person_id: int) -> bool:
        model = await self._session.get(PersonModel, person_id)
        if model is None:
            return False
        await self._session.delete(model)
        await self._session.commit()
        return True

