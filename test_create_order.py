from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_create_order_as_admin():
    users_data = {
        "username": "sayed",
        "password": "g=z%UY334FzY",
    }
    user_response = client.post("/token", data=users_data)
    access_token = user_response.json()["access_token"]
    headers = {"Authorization": f"bearer {access_token}"}

    response = client.post(
        "/orders/",
        json={"product_id": 1, "quantity": 1, "discount": 50},
        headers=headers,
    )

    assert response.status_code == 200


def test_create_order_as_customer():
    users_data = {
        "username": "reda",
        "password": "KA5=u33|@]8t",
    }
    user_response = client.post("/token", data=users_data)
    access_token = user_response.json()["access_token"]
    headers = {"Authorization": f"bearer {access_token}"}

    response = client.post(
        "/orders/",
        json={"product_id": 1, "quantity": 1, "discount": 50},
        headers=headers,
    )
    assert response.status_code == 400


def test_create_order_as_guest():
    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": 1,
            "email": "guest@example.com",
        },
    )
    assert response.status_code == 401
