
# =============================================================================
#  Helpers
# =============================================================================


def _create_article(client, token, title="Test Article", content="Test content"):
    return client.post(
        "/articles",
        json={"title": title, "content": content, "status": "published"},
        headers={"Authorization": f"Bearer {token}"},
    )


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# =============================================================================
#  Auth
# =============================================================================


def test_articles_require_auth(client):
    response = client.get("/articles")
    assert response.status_code == 401

# =============================================================================
#  Create
# =============================================================================


def test_create_article(client, user_token, test_users):
    response = _create_article(client, user_token)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["owner_id"] == test_users[2].id


def test_create_article_default_draft(client, user_token):
    response = client.post(
        "/articles",
        json={"title": "Draft", "content": "Some content"},
        headers=_auth_header(user_token),
    )
    assert response.status_code == 201
    assert response.json()["status"] == "draft"

# =============================================================================
#  List
# =============================================================================


def test_list_articles(client, user_token):
    _create_article(client, user_token, title="Article 1")
    _create_article(client, user_token, title="Article 2")
    response = client.get("/articles", headers=_auth_header(user_token))
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_articles_pagination(client, user_token):
    for i in range(5):
        _create_article(client, user_token, title=f"Article {i}")
    response = client.get(
        "/articles?limit=2&offset=0", headers=_auth_header(user_token)
    )
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5


def test_list_articles_search(client, user_token):
    _create_article(client, user_token, title="Python Guide", content="Learn Python")
    _create_article(client, user_token, title="Java Guide", content="Learn Java")
    response = client.get(
        "/articles?search=Python", headers=_auth_header(user_token)
    )
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Python Guide"

# =============================================================================
#  Get by ID
# =============================================================================


def test_get_article_by_id(client, user_token):
    create_resp = _create_article(client, user_token)
    article_id = create_resp.json()["id"]
    response = client.get(
        f"/articles/{article_id}", headers=_auth_header(user_token)
    )
    assert response.status_code == 200
    assert response.json()["id"] == article_id


def test_get_article_not_found(client, user_token):
    response = client.get("/articles/9999", headers=_auth_header(user_token))
    assert response.status_code == 404

# =============================================================================
#  Update
# =============================================================================


def test_update_own_article_user(client, user_token):
    create_resp = _create_article(client, user_token)
    article_id = create_resp.json()["id"]
    response = client.put(
        f"/articles/{article_id}",
        json={"title": "Updated"},
        headers=_auth_header(user_token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_other_article_user_forbidden(client, user_token, admin_token):
    create_resp = _create_article(client, admin_token)
    article_id = create_resp.json()["id"]
    response = client.put(
        f"/articles/{article_id}",
        json={"title": "Hacked"},
        headers=_auth_header(user_token),
    )
    assert response.status_code == 403


def test_update_other_article_editor(client, editor_token, admin_token):
    create_resp = _create_article(client, admin_token)
    article_id = create_resp.json()["id"]
    response = client.put(
        f"/articles/{article_id}",
        json={"title": "Editor Updated"},
        headers=_auth_header(editor_token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Editor Updated"


def test_update_other_article_admin(client, admin_token, user_token):
    create_resp = _create_article(client, user_token)
    article_id = create_resp.json()["id"]
    response = client.put(
        f"/articles/{article_id}",
        json={"title": "Admin Updated"},
        headers=_auth_header(admin_token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Admin Updated"

# =============================================================================
#  Delete
# =============================================================================


def test_delete_own_article_user(client, user_token):
    create_resp = _create_article(client, user_token)
    article_id = create_resp.json()["id"]
    response = client.delete(
        f"/articles/{article_id}", headers=_auth_header(user_token)
    )
    assert response.status_code == 204


def test_delete_other_article_user_forbidden(client, user_token, admin_token):
    create_resp = _create_article(client, admin_token)
    article_id = create_resp.json()["id"]
    response = client.delete(
        f"/articles/{article_id}", headers=_auth_header(user_token)
    )
    assert response.status_code == 403


def test_delete_article_editor_forbidden(client, editor_token, admin_token):
    create_resp = _create_article(client, admin_token)
    article_id = create_resp.json()["id"]
    response = client.delete(
        f"/articles/{article_id}", headers=_auth_header(editor_token)
    )
    assert response.status_code == 403


def test_delete_article_admin(client, admin_token, user_token):
    create_resp = _create_article(client, user_token)
    article_id = create_resp.json()["id"]
    response = client.delete(
        f"/articles/{article_id}", headers=_auth_header(admin_token)
    )
    assert response.status_code == 204
