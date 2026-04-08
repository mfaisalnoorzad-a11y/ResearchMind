def test_create_article(client):
    response = client.post("/articles", json={
        "url": "https://example.com/test-article",
        "title": "Test Article"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["id"] is not None

def test_get_articles(client):
    client.post("/articles", json={"url": "https://example.com/a1", "title": "Article 1"})
    client.post("/articles", json={"url": "https://example.com/a2", "title": "Article 2"})
    response = client.get("/articles")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["articles"]) == 2

def test_get_article_by_id(client):
    create = client.post("/articles", json={"url": "https://example.com/single", "title": "Single"})
    article_id = create.json()["id"]
    response = client.get(f"/articles/{article_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Single"

def test_get_article_not_found(client):
    response = client.get("/articles/9999")
    assert response.status_code == 404

def test_update_article(client):
    create = client.post("/articles", json={"url": "https://example.com/update", "title": "Update Me"})
    article_id = create.json()["id"]
    response = client.patch(f"/articles/{article_id}", json={"tags": "science", "notes": "important"})
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == "science"
    assert data["notes"] == "important"

def test_update_article_not_found(client):
    response = client.patch("/articles/9999", json={"tags": "nothing"})
    assert response.status_code == 404

def test_delete_article(client):
    create = client.post("/articles", json={"url": "https://example.com/delete", "title": "Delete Me"})
    article_id = create.json()["id"]
    response = client.delete(f"/articles/{article_id}")
    assert response.status_code == 204

def test_delete_article_not_found(client):
    response = client.delete("/articles/9999")
    assert response.status_code == 404

def test_duplicate_url(client):
    client.post("/articles", json={"url": "https://example.com/dupe", "title": "First"})
    response = client.post("/articles", json={"url": "https://example.com/dupe", "title": "Second"})
    assert response.status_code == 409
