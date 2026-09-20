from fastapi.testclient import TestClient

from app.api.dependencies import get_person_repository
from app.domain.person import Person
from app.main import app
from app.repositories.memory import InMemoryPersonRepository


def make_client() -> TestClient:
    repository = InMemoryPersonRepository(
        [Person(id=1, name="Existing", age=20, address="Moscow", work="Student")]
    )
    app.dependency_overrides[get_person_repository] = lambda: repository
    return TestClient(app)


def test_get_demo_person() -> None:
    with make_client() as client:
        response = client.get("/api/v1/persons/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Existing"


def test_get_unknown_person_returns_404() -> None:
    with make_client() as client:
        response = client.get("/api/v1/persons/999")

    assert response.status_code == 404


def test_create_person_returns_location() -> None:
    with make_client() as client:
        response = client.post(
            "/api/v1/persons",
            json={"name": "New person", "age": 25},
        )

    assert response.status_code == 201
    assert response.content == b""
    assert response.headers["location"] == "/api/v1/persons/2"


def test_patch_preserves_omitted_fields() -> None:
    with make_client() as client:
        response = client.patch(
            "/api/v1/persons/1",
            json={"name": "Updated"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Updated",
        "age": 20,
        "address": "Moscow",
        "work": "Student",
    }


def test_delete_person() -> None:
    with make_client() as client:
        delete_response = client.delete("/api/v1/persons/1")
        get_response = client.get("/api/v1/persons/1")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404

