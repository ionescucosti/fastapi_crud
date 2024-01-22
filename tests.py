from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '<a href="/docs">Swagger</a></h2></br><a href="/login">login</a>'


def test_create_new_account():
    payload = {
            "name": "test"
        }
    response = client.post(
        "/account/",
        headers={"X-Token": "coneofsilence"},
        json=payload,
    )
    assert response.status_code == 201
    assert response.json() == payload


def test_get_accounts():
    response = client.get("/accounts/")
    assert response.status_code == 200
    assert response.json()[0]['name'] == 'test'


def test_get_account():
    account_name = "test"
    response = client.get(f"/account/{account_name}")
    assert response.status_code == 200
    assert response.json()['name'] == account_name


def test_get_non_existing_account():
    account_name = "test"
    response = client.get(f"/accounts/{account_name}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_create_existing_account():
    response = client.post(
        "/account/",
        headers={"X-Token": "qwewrtyyiio"},
        json={
            "name": "test"
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Account already registered"}


def test_delete_account():
    account_name = "test"
    response = client.delete(
        f"/account/{account_name}",
        headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 200
    assert response.json()['name'] == account_name


def test_delete_non_existing_account():
    account_name = "test"
    response = client.delete(
        f"/account/{account_name}",
        headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Account not registered"}


