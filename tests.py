from fastapi.testclient import TestClient

from routes import app

client = TestClient(app)


# def test_simple():
#     assert True


def test_read_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200


def test_read_recipes_id():
    response = client.get("/recipes/1")
    assert response.status_code == 200


def test_read_recipes_bad_id_validation_error():
    response = client.get("/recipes/id")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "recipe_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "id",
            }
        ]
    }


def test_create_item():
    body = {
        "name": "recipe name",
        "cooking_time": 150,
        "ingredients": "apple orange",
        "description": "description, description, description",
    }
    response = client.post("/recipes", json=body)
    assert response.status_code == 201
    assert (
        response.json()["name"] == "recipe name"
        and response.json()["cooking_time"] == 150
        and response.json()["ingredients"] == "apple orange"
        and response.json()["description"] == "description, description, description"
        and type(response.json()["id"]) == int
    )


def test_create_item_validation_error():
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
