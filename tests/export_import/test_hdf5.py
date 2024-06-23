import h5py
from io import BytesIO
from app.model import Order, Status
from datetime import datetime


def test_export_to_hdf5(client, init_orders):
    response = client.get("/api/orders/export/hdf5")
    assert response.status_code == 200
    hdf5 = response.data

    with h5py.File(BytesIO(hdf5), "r") as file:
        orders_group = file["orders"]
        assert len(orders_group.keys()) == 3

        order_1 = orders_group["order_1"]
        assert order_1["id"][()] == 1
        assert order_1["name"][()].decode("utf-8") == init_orders[0].name
        assert order_1["description"][()].decode("utf-8") == init_orders[0].description
        assert order_1["creation_date"][()].decode("utf-8") == init_orders[
            0
        ].creation_date.strftime("%Y-%m-%d %H:%M:%S")
        assert order_1["status"][()].decode("utf-8") == init_orders[0].status

        order_2 = orders_group["order_2"]
        assert order_2["id"][()] == 2
        assert order_2["name"][()].decode("utf-8") == init_orders[1].name
        assert order_2["description"][()].decode("utf-8") == init_orders[1].description
        assert order_2["creation_date"][()].decode("utf-8") == init_orders[
            1
        ].creation_date.strftime("%Y-%m-%d %H:%M:%S")
        assert order_2["status"][()].decode("utf-8") == init_orders[1].status

        order_3 = orders_group["order_3"]
        assert order_3["id"][()] == 3
        assert order_3["name"][()].decode("utf-8") == init_orders[2].name
        assert order_3["description"][()].decode("utf-8") == init_orders[2].description
        assert order_3["creation_date"][()].decode("utf-8") == init_orders[
            2
        ].creation_date.strftime("%Y-%m-%d %H:%M:%S")
        assert order_3["status"][()].decode("utf-8") == init_orders[2].status


def test_import_from_hdf5(client, init_orders):
    hdf5 = prepare_example_h5_file()

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


def prepare_example_h5_file():
    new_order = Order(
        name="Order new",
        description="Description new",
        creation_date=datetime(2024, 6, 21, 11, 11, 11),
        status=Status.COMPLETED.value,
    )
    id = 4

    hdf5 = BytesIO()
    with h5py.File(hdf5, "w") as file:
        orders_group = file.create_group("orders")
        order_group = orders_group.create_group(f"order_{id}")
        order_group.create_dataset("id", data=id)
        order_group.create_dataset("name", data=new_order.name)
        order_group.create_dataset("description", data=new_order.description)
        order_group.create_dataset(
            "creation_date",
            data=new_order.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        )
        order_group.create_dataset("status", data=new_order.status)

    hdf5.seek(0)
    return hdf5
