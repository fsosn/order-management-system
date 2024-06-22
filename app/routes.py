from flask import Blueprint, request, send_file
from .services import order_service, report_service

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    response, status_code = order_service.create_order(data)
    return response, status_code


@orders_bp.route("/api/orders/<int:id>", methods=["GET"])
def get_order(id):
    response, status_code = order_service.get_order(id)
    return response, status_code


@orders_bp.route("/api/orders", methods=["GET"])
def get_orders():
    response, status_code = order_service.get_orders()
    return response, status_code


@orders_bp.route("/api/orders/<int:id>", methods=["PUT"])
def update_order(id):
    data = request.get_json()
    response, status_code = order_service.update_order(id, data)
    return response, status_code


@orders_bp.route("/api/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    response, status_code = order_service.delete_order(id)
    return response, status_code


@orders_bp.route("/api/orders/statistics", methods=["GET"])
def get_statistics():
    response, status_code = order_service.get_statistics()
    return response, status_code


@orders_bp.route("/api/orders/xlsx-report", methods=["GET"])
def generate_xlsx_report():
    xlxs_report = report_service.generate_xlsx_report()
    return send_file(
        xlxs_report,
        download_name="orders_report.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
