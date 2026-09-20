import asyncio
from dataclasses import replace
from typing import Any

from app.domain.person import Person
from app.repositories.person import PersonRepository


class InMemoryPersonRepository(PersonRepository):
    """Temporary repository for checking the API without PostgreSQL."""

    def __init__(self, persons: list[Person] | None = None) -> None:
        initial_persons = persons or []
        self._persons = {
            person.id: person
            for person in initial_persons
            if person.id is not None
        }
        self._next_id = max(self._persons, default=0) + 1
        self._lock = asyncio.Lock()

    @classmethod
    def with_demo_person(cls) -> "InMemoryPersonRepository":
        return cls(
            [
                Person(
                    id=1,
                    name="Ivan Ivanov",
                    age=30,
                    address="Moscow",
                    work="Engineer",
                )
            ]
        )

    async def get_by_id(self, person_id: int) -> Person | None:
        person = self._persons.get(person_id)
        return replace(person) if person is not None else None

    async def get_all(self) -> list[Person]:
        return [replace(person) for person in self._persons.values()]

    async def create(self, person: Person) -> Person:
        async with self._lock:
            created = replace(person, id=self._next_id)
            self._persons[self._next_id] = created
            self._next_id += 1
        return replace(created)

    async def update(self, person_id: int, changes: dict[str, Any]) -> Person | None:
        async with self._lock:
            current = self._persons.get(person_id)
            if current is None:
                return None
            updated = replace(current, **changes)
            self._persons[person_id] = updated
        return replace(updated)

    async def delete(self, person_id: int) -> bool:
        async with self._lock:
            return self._persons.pop(person_id, None) is not None

