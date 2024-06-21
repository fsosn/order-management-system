from flask import Blueprint, request
from . import service

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    response, status_code = service.create_order(data)
    return response, status_code


@orders_bp.route("/api/orders/<int:id>", methods=["GET"])
def get_order(id):
    response, status_code = service.get_order(id)
    return response, status_code


@orders_bp.route("/api/orders", methods=["GET"])
def get_orders():
    response, status_code = service.get_orders()
    return response, status_code


@orders_bp.route("/api/orders/<int:id>", methods=["PUT"])
def update_order(id):
    data = request.get_json()
    response, status_code = service.update_order(id, data)
    return response, status_code


@orders_bp.route("/api/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    response, status_code = service.delete_order(id)
    return response, status_code
