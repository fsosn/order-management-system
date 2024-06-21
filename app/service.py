from flask import jsonify
from .model import Order, Status
from .extensions import db
from .validation import validate_order


def create_order(data):
    errors = validate_order(data)
    if errors:
        return jsonify(errors), 400

    order = Order(
        name=data.get("name"),
        description=data.get("description"),
        status=data.get("status", Status.NEW),
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order created successfully", "id": order.id}), 201


def get_order(id):
    order = Order.query.get_or_404(id)
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
    errors = validate_order(data)
    if errors:
        return jsonify(errors), 400

    order = Order.query.get_or_404(id)
    order.name = data.get("name", order.name)
    order.description = data.get("description", order.description)
    order.status = data.get("status", order.status)
    db.session.commit()
    return jsonify({"message": "Order updated successfully."}), 200


def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"Order deleted successfully."}), 200
