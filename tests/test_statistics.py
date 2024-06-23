from app.model import Status


def test_get_statistics(client, init_orders):
    response = client.get("/api/orders/statistics")
    assert response.status_code == 200
    data = response.get_json()

    assert "total_orders" in data
    assert data["total_orders"] == len(init_orders)

    assert "status" in data
    status_counts = data["status"]
    expected_counts = {
        Status.NEW.value: 1,
        Status.IN_PROGRESS.value: 1,
        Status.COMPLETED.value: 1,
    }

    for status, count in expected_counts.items():
        assert status in status_counts
        assert status_counts[status] == count


def test_get_statistics_no_orders(client):
    response = client.get("/api/orders/statistics")
    assert response.status_code == 200
    data = response.get_json()

    assert "total_orders" in data
    assert data["total_orders"] == 0

    assert "status" in data
    status_counts = data["status"]
    expected_counts = {
        Status.NEW.value: 0,
        Status.IN_PROGRESS.value: 0,
        Status.COMPLETED.value: 0,
    }

    for status, count in expected_counts.items():
        assert status in status_counts
        assert status_counts[status] == count
