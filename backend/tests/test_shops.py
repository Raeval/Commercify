from enums import GenderType, ShopPlan

def test_create_shop_no_plan(client):
    access_token, user_id = get_token_and_user_id(client)

    res = client.post(
        "/shops/create",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json = {
            "shop_name": "Test shop"
        }
    )

    assert res.status_code == 201

    shop_id = res.json()["shop_id"]

    # Get shop from database
    res = client.get(
        f"/shops/{shop_id}",
        headers={
                    "Authorization": f"Bearer {access_token}"
        },
    )
    shop = res.json()
    assert shop["shop_name"] == "Test shop"
    assert any(owner["user_id"] == user_id for owner in shop["owners"])

def test_create_with_plan(client):
    access_token, user_id = get_token_and_user_id(client)

    res = client.post(
        "/shops/create",
        headers = {
            "Authorization": f"Bearer {access_token}"
        },
        json = {
            "shop_name": "Test shop",
            "plan": ShopPlan.PREMIUM
        }
    )

    shop_id = res.json()["shop_id"]

    res = client.get(
        f"/shops/{shop_id}",
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
    )
    
    shop = res.json()
    assert shop["shop_name"] == "Test shop"
    assert any(owner["user_id"] == user_id for owner in shop["owners"])

def get_token_and_user_id(client):
    res = client.post(
            "/auth/register",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "test123",
                "gender": GenderType.MALE
            }
        )

    access_token = res.json()["access_token"]

    res = client.get(
        "/auth/me",
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
    )
    user_id = res.json()["user_id"]
    return access_token, user_id