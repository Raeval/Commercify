from enums import GenderType

def test_register_user(client):
    res = client.post(
        "/auth/register",
        json={
            "username": "test",
            "email": "test@example.com",
            "password": "test123",
            "gender": GenderType.MALE
        }
    )

    assert res.status_code == 201

    res = res.json()
    access_token = res["access_token"]

    res = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    res = res.json()
    assert res["username"] == "test"

def test_register_duplicate(client):
    client.post(
        "/auth/register",
        json={
            "username": "test",
            "email": "test@example.com",
            "password": "test123",
            "gender": GenderType.MALE
        }
    )

    res = client.post(
            "/auth/register",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "test123",
                "gender": GenderType.MALE
            }
        )

    assert res.status_code == 409

def test_sign_in(client):
    client.post(
            "/auth/register",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "test123",
                "gender": GenderType.MALE
            }
        )
    
    res = client.post(
        "auth/sign-in",
        json={
            "username": "test",
            "password": "test123"
        }
    )

    res = res.json()
    access_token = res["access_token"]

    res = client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
    )

    res = res.json()
    assert res["username"] == "test"

def test_no_user_sign_in(client):
    res = client.post(
        "auth/sign-in",
        json={
            "username": "test",
            "password": "test123"
        }
    )

    assert res.status_code == 401

def test_sign_in_wrong_password(client):
    client.post(
        "/auth/register",
        json = {
            "username": "test",
            "email": "test@example.com",
            "password": "test123",
            "gender": GenderType.MALE
        }
    )

    res = client.post(
        "/auth/sign-in",
        json = {
            "username": "test",
            "password": "wrongpassword",
        }
    )
    assert res.status_code == 401