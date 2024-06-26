from flask import jsonify
from app.model import Order, Status
from app.extensions import db
from .utils.validation import validate_request_data, validate_order_data
import pandas as pd


def create_order(data):
    errors = validate_request_data(data)
    if errors["errors"]:
        return jsonify(errors), 400

    order = Order(
        name=data.get("name"),
        description=data.get("description"),
        status=data.get("status", Status.NEW.value),
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order created successfully", "id": order.id}), 201


def get_order(id):
    order = db.session.get(Order, id)

    if order is None:
        return jsonify({"message": f"Order not found."}), 404

    return (
        jsonify(
            {
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "creation_date": order.creation_date,
                "status": order.status.value,
            }
        ),
        200,
    )


def get_orders():
    orders = Order.query.all()

    orders_list = [
        {
            "id": str(order.id),
            "name": order.name,
            "description": order.description,
            "creation_date": order.creation_date,
            "status": order.status.value,
        }
        for order in orders
    ]

    return jsonify(orders_list), 200


def update_order(id, data):
    errors = validate_order_data(data)
    if errors["errors"]:
        return jsonify(errors), 400

    order = db.session.get(Order, id)
    if order is None:
        return jsonify({"message": f"Order not found."}), 404

    if "name" in data:
        order.name = data.get("name", order.name)
    if "description" in data:
        order.description = data.get("description", order.description)
    if "status" in data:
        order.status = data.get("status", order.status)
    db.session.commit()

    return jsonify({"message": "Order updated successfully."}), 200


def bulk_update_statuses(id_list, status):
    if not isinstance(id_list, list) or not all(isinstance(i, int) for i in id_list):
        return jsonify({"error": "Property 'id_list' must be a list of integers."}), 400

    try:
        status = Status(status)
    except ValueError:
        return (
            jsonify(
                {
                    "error": f"Invalid status value. Choose one of: {', '.join([s.value for s in Status])}"
                }
            ),
            400,
        )

    updated_orders = []
    not_found_orders = []
    no_change_orders = []

    for i in id_list:
        order = db.session.get(Order, i)
        try:
            if order.status.value != status.value:
                order.status = status
                updated_orders.append(i)
            else:
                no_change_orders.append(i)
        except Exception:
            not_found_orders.append(i)
            continue

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Completed bulk update of statuses.",
                "updated": updated_orders,
                "no_change": no_change_orders,
                "not_found": not_found_orders,
            }
        ),
        200,
    )


def delete_order(id):
    order = db.session.get(Order, id)
    if order is None:
        return jsonify({"message": f"Order not found."}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": f"Order deleted successfully."}), 200


def get_statistics():
    orders = Order.query.all()

    status_values = [status.value for status in Status]

    data = {
        "status": [order.status.value for order in orders],
    }
    df = pd.DataFrame(data)

    status_counts = df["status"].value_counts().to_dict()

    for status in status_values:
        if status not in status_counts:
            status_counts[status] = 0

    return jsonify({"total_orders": len(df.index), "status": status_counts}), 200
