from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_auth_attempts_limit_5():
    user_data = {
        "username": "reda",
    }
    # 1
    user_data.update({"password": "58f8e745"})
    client.post("/token", data=user_data)
    # 2
    user_data.update({"password": "58f8e745"})
    client.post("/token", data=user_data)
    # 3
    user_data.update({"password": "82f3d7fc"})
    client.post("/token", data=user_data)
    # 4
    user_data.update({"password": "d262fe72"})
    client.post("/token", data=user_data)
    # 5
    user_data.update({"password": "aee0235a"})
    client.post("/token", data=user_data)
    # 6
    user_data.update({"password": "KA5=u33|@]8t"})
    response = client.post("/token", data=user_data)
    assert response.status_code == 401
