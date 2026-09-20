from abc import ABC, abstractmethod
from typing import Any

from app.domain.person import Person


class PersonRepository(ABC):
    """Persistence port used by the service layer."""

    @abstractmethod
    async def get_by_id(self, person_id: int) -> Person | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[Person]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, person: Person) -> Person:
        raise NotImplementedError

    @abstractmethod
    async def update(self, person_id: int, changes: dict[str, Any]) -> Person | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, person_id: int) -> bool:
        raise NotImplementedError

