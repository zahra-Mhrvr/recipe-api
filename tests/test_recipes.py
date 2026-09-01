def make_recipe(client, **overrides):
    payload = {
        "title": "Pancakes",
        "ingredients": ["flour", "eggs", "milk"],
        "instructions": "Mix everything and fry on medium heat.",
        "prep_minutes": 15,
        "servings": 2,
    }
    payload.update(overrides)
    return client.post("/recipes/", json=payload)


def test_create_recipe(client):
    resp = make_recipe(client)
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Pancakes"
    assert body["ingredients"] == ["flour", "eggs", "milk"]
    assert "id" in body


def test_get_recipe(client):
    created = make_recipe(client).json()
    resp = client.get(f"/recipes/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Pancakes"


def test_get_recipe_not_found(client):
    resp = client.get("/recipes/999")
    assert resp.status_code == 404


def test_search_by_ingredient(client):
    make_recipe(client, title="Pancakes")
    make_recipe(client, title="Omelette", ingredients=["eggs", "cheese"])
    make_recipe(client, title="Salad", ingredients=["lettuce", "tomato"])

    resp = client.get("/recipes/?ingredient=eggs")
    titles = [r["title"] for r in resp.json()]

    assert resp.status_code == 200
    assert set(titles) == {"Pancakes", "Omelette"}


def test_update_recipe(client):
    created = make_recipe(client).json()
    resp = client.patch(f"/recipes/{created['id']}", json={"servings": 4})

    assert resp.status_code == 200
    assert resp.json()["servings"] == 4
    assert resp.json()["title"] == "Pancakes"  # untouched fields stay the same


def test_delete_recipe(client):
    created = make_recipe(client).json()
    resp = client.delete(f"/recipes/{created['id']}")
    assert resp.status_code == 204

    follow_up = client.get(f"/recipes/{created['id']}")
    assert follow_up.status_code == 404


def test_negative_prep_time_rejected(client):
    resp = make_recipe(client, prep_minutes=-10)
    assert resp.status_code == 422
