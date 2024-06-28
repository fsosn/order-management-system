import h5py
from io import BytesIO
from app.model import Order, Status
from datetime import datetime
from app.extensions import db


def test_export_to_hdf5(client, init_orders):
    response = client.get("/api/orders/export/hdf5")
    assert response.status_code == 200
    hdf5 = response.data

    with h5py.File(BytesIO(hdf5), "r") as file:
        assert len(file.keys()) == len(init_orders)

        for i in range(1, len(init_orders) + 1):
            order = db.session.get(Order, i)
            order_group = file[f"order_{order.id}"]
            assert order_group.attrs["id"] == order.id
            assert order_group.attrs["name"] == order.name
            assert order_group.attrs["description"] == order.description
            assert order_group.attrs["creation_date"] == order.creation_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            assert order_group.attrs["status"] == order.status.value


def test_import_from_hdf5(client, init_orders):
    hdf5 = __prepare_example_hdf5_file()

    response = client.post(
        "/api/orders/import/hdf5",
        data=dict(file=(hdf5, "orders.h5")),
        content_type="multipart/form-data",
    )

    assert response.status_code == 200

    orders = Order.query.all()
    assert len(orders) == len(init_orders) + 1

    imported_order = orders[-1]
    assert imported_order.name == "Order new"
    assert imported_order.description == "Description new"
    assert imported_order.creation_date.strftime("%Y-%m-%d %H:%M:%S") == datetime(
        2024, 6, 21, 11, 11, 11
    ).strftime("%Y-%m-%d %H:%M:%S")
    assert imported_order.status.value == Status.COMPLETED.value


def __prepare_example_hdf5_file():
    new_order = Order(
        name="Order new",
        description="Description new",
        creation_date=datetime(2024, 6, 21, 11, 11, 11),
        status=Status.COMPLETED.value,
    )
    order_id = 4

    hdf5 = BytesIO()
    with h5py.File(hdf5, "w") as file:
        order_group = file.create_group(f"order_{order_id}")
        order_group.attrs["id"] = order_id
        order_group.attrs["name"] = new_order.name
        order_group.attrs["description"] = new_order.description
        order_group.attrs["creation_date"] = new_order.creation_date.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        order_group.attrs["status"] = new_order.status

    hdf5.seek(0)
    return hdf5
