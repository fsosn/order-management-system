from app.model import Order, Status
from app.extensions import db


def test_update_order_valid(client, init_orders):
    response = client.put(
        "/api/orders/1",
        json={
            "name": "Updated Name",
            "description": "Updated Description",
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 200

    updated_order = db.session.get(Order, 1)
    assert updated_order.name == "Updated Name"
    assert updated_order.description == "Updated Description"
    assert updated_order.status.value == Status.COMPLETED.value


def test_update_order_valid_no_change(client, init_orders):
    response = client.put(
        "/api/orders/1",
        json={
            "name": init_orders[0].name,
            "description": init_orders[0].description,
            "status": init_orders[0].status,
        },
    )
    assert response.status_code == 200

    updated_order = db.session.get(Order, 1)
    assert updated_order.name == init_orders[0].name
    assert updated_order.description == init_orders[0].description
    assert updated_order.status.value == init_orders[0].status


def test_update_order_invalid_status(client, init_orders):
    response = client.put(
        "/api/orders/1",
        json={
            "name": "Updated Name",
            "description": "Updated Description",
            "status": "TEST",
        },
    )
    assert response.status_code == 400


def test_update_order_fields_too_long(client, init_orders):
    response = client.put(
        "/api/orders/1",
        json={
            "name": "a" * 129,
            "description": "Updated Description",
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 400

    response = client.put(
        "/api/orders/1",
        json={
            "name": "Updated Name",
            "description": "a" * 257,
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 400


def test_bulk_update_statuses_valid(client, init_orders):
    response = client.put(
        "/api/orders",
        json={
            "id_list": [1, 2],
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["updated"] == [1, 2]
    assert data["no_change"] == []
    assert data["not_found"] == []

    order_1 = db.session.get(Order, 1)
    assert order_1.status.value == Status.COMPLETED.value
    order_2 = db.session.get(Order, 2)
    assert order_2.status.value == Status.COMPLETED.value


def test_bulk_update_statuses_valid_no_change(client, init_orders):
    response = client.put(
        "/api/orders",
        json={
            "id_list": [3],
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["updated"] == []
    assert data["no_change"] == [3]
    assert data["not_found"] == []
    order_3 = db.session.get(Order, 3)
    assert order_3.status.value == init_orders[2].status


def test_bulk_update_statuses_valid_not_found(client, init_orders):
    response = client.put(
        "/api/orders",
        json={
            "id_list": [4, 5, 6],
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["updated"] == []
    assert data["no_change"] == []
    assert data["not_found"] == [4, 5, 6]


def test_bulk_update_statuses_valid_updated_no_change_not_found(client, init_orders):
    response = client.put(
        "/api/orders",
        json={
            "id_list": [1, 2, 3, 4],
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["updated"] == [1, 2]
    assert data["no_change"] == [3]
    assert data["not_found"] == [4]
    order_1 = db.session.get(Order, 1)
    assert order_1.status.value == Status.COMPLETED.value
    order_2 = db.session.get(Order, 2)
    assert order_2.status.value == Status.COMPLETED.value
    order_3 = db.session.get(Order, 3)
    assert order_3.status.value == init_orders[2].status


def test_bulk_update_statuses_invalid_id_list(client):
    response = client.put(
        "/api/orders",
        json={
            "id_list": ["a", "b", "c"],
            "status": Status.COMPLETED.value,
        },
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_bulk_update_statuses_invalid_status(client):
    response = client.put(
        "/api/orders",
        json={
            "id_list": [1, 2],
            "status": "TEST",
        },
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_bulk_update_statuses_missing_properties(client):
    response = client.put(
        "/api/orders",
        json={},
    )
    assert response.status_code == 400
    assert "error" in response.get_json()
