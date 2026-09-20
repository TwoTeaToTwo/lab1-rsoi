from dataclasses import dataclass


@dataclass(slots=True)
class Person:
    id: int | None
    name: str
    age: int | None = None
    address: str | None = None
    work: str | None = None

