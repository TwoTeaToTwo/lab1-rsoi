from typing import Annotated

from fastapi import Depends

from app.repositories.memory import InMemoryPersonRepository
from app.repositories.person import PersonRepository
from app.services.person import PersonService


# One repository instance is intentionally kept for the whole process so that
# objects created through the API remain available between requests.
_person_repository = InMemoryPersonRepository.with_demo_person()


def get_person_repository() -> PersonRepository:
    return _person_repository


PersonRepositoryDependency = Annotated[
    PersonRepository,
    Depends(get_person_repository),
]


def get_person_service(
    repository: PersonRepositoryDependency,
) -> PersonService:
    return PersonService(repository)


PersonServiceDependency = Annotated[PersonService, Depends(get_person_service)]

