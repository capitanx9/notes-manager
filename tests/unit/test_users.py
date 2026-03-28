
# =============================================================================
#  Helpers
# =============================================================================


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# =============================================================================
#  Auth
# =============================================================================


def test_users_require_auth(client):
    response = client.get("/users")
    assert response.status_code == 401

# =============================================================================
#  Me
# =============================================================================


def test_get_me_user(client, user_token, test_users):
    response = client.get("/users/me", headers=_auth_header(user_token))
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@test.com"
    assert "hashed_password" not in data


def test_get_me_admin(client, admin_token, test_users):
    response = client.get("/users/me", headers=_auth_header(admin_token))
    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.com"

# =============================================================================
#  List
# =============================================================================


def test_list_users_admin(client, admin_token, test_users):
    response = client.get("/users", headers=_auth_header(admin_token))
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


def test_list_users_user_forbidden(client, user_token, test_users):
    response = client.get("/users", headers=_auth_header(user_token))
    assert response.status_code == 403


def test_list_users_editor_forbidden(client, editor_token, test_users):
    response = client.get("/users", headers=_auth_header(editor_token))
    assert response.status_code == 403


def test_list_users_search(client, admin_token, test_users):
    response = client.get("/users?search=admin", headers=_auth_header(admin_token))
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["email"] == "admin@test.com"


def test_list_users_pagination(client, admin_token, test_users):
    response = client.get("/users?limit=1", headers=_auth_header(admin_token))
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 3

# =============================================================================
#  Get by ID
# =============================================================================


def test_get_user_by_id_admin(client, admin_token, test_users):
    user_id = test_users[2].id
    response = client.get(f"/users/{user_id}", headers=_auth_header(admin_token))
    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"


def test_get_user_by_id_user_forbidden(client, user_token, test_users):
    user_id = test_users[0].id
    response = client.get(f"/users/{user_id}", headers=_auth_header(user_token))
    assert response.status_code == 403


def test_get_user_not_found(client, admin_token, test_users):
    response = client.get("/users/9999", headers=_auth_header(admin_token))
    assert response.status_code == 404

# =============================================================================
#  Update
# =============================================================================


def test_update_self_user(client, user_token, test_users):
    user_id = test_users[2].id
    response = client.put(
        f"/users/{user_id}",
        json={"first_name": "Updated"},
        headers=_auth_header(user_token),
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"


def test_update_other_user_forbidden(client, user_token, test_users):
    admin_id = test_users[0].id
    response = client.put(
        f"/users/{admin_id}",
        json={"first_name": "Hacked"},
        headers=_auth_header(user_token),
    )
    assert response.status_code == 403


def test_update_any_user_admin(client, admin_token, test_users):
    user_id = test_users[2].id
    response = client.put(
        f"/users/{user_id}",
        json={"first_name": "Admin Updated"},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Admin Updated"


def test_update_role_user_forbidden(client, user_token, test_users):
    user_id = test_users[2].id
    response = client.put(
        f"/users/{user_id}",
        json={"role": "admin"},
        headers=_auth_header(user_token),
    )
    assert response.status_code == 403


def test_update_role_admin(client, admin_token, test_users):
    user_id = test_users[2].id
    response = client.put(
        f"/users/{user_id}",
        json={"role": "editor"},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 200
    assert response.json()["role"] == "editor"

# =============================================================================
#  Delete
# =============================================================================


def test_delete_user_admin(client, admin_token, test_users):
    user_id = test_users[2].id
    response = client.delete(f"/users/{user_id}", headers=_auth_header(admin_token))
    assert response.status_code == 204


def test_delete_user_forbidden(client, user_token, test_users):
    admin_id = test_users[0].id
    response = client.delete(f"/users/{admin_id}", headers=_auth_header(user_token))
    assert response.status_code == 403


def test_delete_self_admin(client, admin_token, test_users):
    admin_id = test_users[0].id
    response = client.delete(f"/users/{admin_id}", headers=_auth_header(admin_token))
    assert response.status_code == 400
