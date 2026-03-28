def test_login_success(client, test_users):
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_users):
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_nonexistent_email(client, test_users):
    response = client.post("/auth/login", json={
        "email": "nobody@test.com",
        "password": "password123",
    })
    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/liveness")
    assert response.status_code == 200


def test_login_all_roles(client, test_users):
    for email in ["admin@test.com", "editor@test.com", "user@test.com"]:
        response = client.post("/auth/login", json={
            "email": email,
            "password": "password123",
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
