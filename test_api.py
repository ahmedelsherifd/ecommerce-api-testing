from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_update_product_as_admin():
    admin_data = {
        "username": "sayed",
        "password": "g=z%UY334FzY",
    }
    response = client.post("/token", data=admin_data)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"bearer {access_token}"}
    response = client.post("/products/1", json={"price": 0}, headers=headers)
    assert response.status_code == 200


def test_update_product_as_customer():
    admin_data = {
        "username": "reda",
        "password": "KA5=u33|@]8t",
    }
    response = client.post("/token", data=admin_data)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"bearer {access_token}"}
    response = client.post("/products/1", json={"price": 0}, headers=headers)
    assert response.status_code == 403


def test_update_product_as_guest():
    response = client.post("/products/1", json={"price": 0})
    assert response.status_code == 401
    # assert response.json() == {"msg": "Hello World"}
