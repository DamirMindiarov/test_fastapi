import pytest
from fastapi.testclient import TestClient

from app.routes import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_read_recipes(client):
    response = client.get("/recipes")
    assert response.status_code == 200


def test_read_recipes_id(client):
    response = client.get("/recipes/1")
    assert response.status_code == 200


def test_read_recipes_bad_id_validation_error(client):
    response = client.get("/recipes/id")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "recipe_id"],
                "msg": "Input should be a valid integer, "
                "unable to parse string as an integer",
                "input": "id",
            }
        ]
    }


def test_create_item(client):
    body = {
        "name": "recipe name",
        "cooking_time": 150,
        "ingredients": "apple orange",
        "description": "description, description, description",
    }
    response = client.post("/recipes", json=body)
    body.update(id=response.json()["id"])

    assert response.status_code == 201
    assert response.json() == body
    assert response.json()["id"]


def test_create_item_validation_error(client):
    body = {
        "name": 11111,
        "cooking_time": 150,
        "ingredients": "apple orange",
        "description": "description, description, description",
    }
    response = client.post("/recipes", json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_type",
                "loc": ["body", "name"],
                "msg": "Input should be a valid string",
                "input": 11111,
            }
        ]
    }
