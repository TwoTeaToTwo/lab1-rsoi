from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.person import PersonRepository
from app.repositories.sqlalchemy import SqlAlchemyPersonRepository
from app.services.person import PersonService


DbSessionDependency = Annotated[AsyncSession, Depends(get_db_session)]


async def get_person_repository(
    session: DbSessionDependency,
) -> AsyncIterator[PersonRepository]:
    """Build a request-scoped PostgreSQL repository."""
    yield SqlAlchemyPersonRepository(session)


PersonRepositoryDependency = Annotated[
    PersonRepository,
    Depends(get_person_repository),
]


def get_person_service(
    repository: PersonRepositoryDependency,
) -> PersonService:
    return PersonService(repository)


PersonServiceDependency = Annotated[PersonService, Depends(get_person_service)]