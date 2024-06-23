def test_delete_order_valid(client, init_orders):
    response = client.delete("/api/orders/1")
    assert response.status_code == 200
    response = client.delete("/api/orders/1")
    assert response.status_code == 404


def test_delete_order_not_found(client):
    response = client.delete("/api/orders/100")
    assert response.status_code == 404
