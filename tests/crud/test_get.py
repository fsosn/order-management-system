def test_get_order_by_id(client, init_orders):
    response = client.get("/api/orders/2")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == init_orders[1].name
    assert data["description"] == init_orders[1].description
    assert data["status"] == init_orders[1].status


def test_get_order_by_id_not_found(client, init_orders):
    response = client.get("/api/orders/100")
    assert response.status_code == 404


def test_get_orders(client, init_orders):
    response = client.get("/api/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == len(init_orders)

    for i, actual in enumerate(data):
        assert actual["name"] == init_orders[i].name
        assert actual["description"] == init_orders[i].description
        assert actual["status"] == init_orders[i].status


def test_get_orders_empty(client):
    response = client.get("/api/orders")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0
