from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_orders_as_admin():
    users_data = {
        "username": "sayed",
        "password": "g=z%UY334FzY",
    }
    response = client.post("/token", data=users_data)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"bearer {access_token}"}
    response = client.get("/orders/", headers=headers)
    assert response.status_code == 200


def test_get_orders_as_customer():
    users_data = {
        "username": "reda",
        "password": "KA5=u33|@]8t",
    }
    response = client.post("/token", data=users_data)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"bearer {access_token}"}
    response = client.get("/orders/", headers=headers)
    assert response.status_code == 200
    orders = response.json()
    for order in orders:
        assert order["customer"]["username"] == "reda"


def test_get_orders_as_guest():
    response = client.get("/orders/")
    assert response.status_code == 401
