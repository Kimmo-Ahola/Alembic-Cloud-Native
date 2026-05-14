def test_create_task(client): # client är en TestClient i FastAPI
    response = client.post("/tasks", json={"title": "Do something"})
    assert response.status_code == 201

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_create_task_failure(client):
    response = client.post("/tasks", json={"title": ""})
    # test validation error. Title can not be empty
    assert response.status_code == 422

def test_create_task_failure_title_too_long(client):
    response = client.post("/tasks", json={"title": 1000*"f"})
    # test validation error. Title can not be empty
    assert response.status_code == 422