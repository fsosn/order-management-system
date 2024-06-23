from app.model import Status


def test_create_order_valid(client):
    response = client.post(
        "/api/orders",
        json={
            "name": "Name",
            "description": "Description",
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1


def test_create_order_missing_required_fields(client):
    response = client.post(
        "/api/orders",
        json={
            "description": "Description",
            "status": Status.IN_PROGRESS.value,
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/api/orders",
        json={
            "name": "Name",
            "status": Status.IN_PROGRESS.value,
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/api/orders",
        json={
            "status": Status.IN_PROGRESS.value,
        },
    )
    assert response.status_code == 400


def test_create_order_invalid_status(client):
    response = client.post(
        "/api/orders",
        json={
            "name": "Name",
            "description": "Description",
            "status": "TEST",
        },
    )
    assert response.status_code == 400


def test_create_order_fields_too_long(client):
    response = client.post(
        "/api/orders",
        json={
            "name": "a" * 129,
            "description": "Description",
            "status": Status.IN_PROGRESS.value,
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/api/orders",
        json={
            "name": "Name",
            "description": "a" * 257,
            "status": Status.IN_PROGRESS.value,
        },
    )
    assert response.status_code == 400
