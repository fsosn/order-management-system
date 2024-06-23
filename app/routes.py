from flask import Blueprint, request, send_file
from .services import order_service, report_service
from flask import jsonify

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


@orders_bp.route("/api/orders/export/xml", methods=["GET"])
def export_to_xml():
    xml = report_service.export_to_xml()
    return send_file(
        xml, download_name="orders.xml", as_attachment=True, mimetype="application/xml"
    )


@orders_bp.route("/api/orders/import/xml", methods=["POST"])
def import_from_xml():
    if "file" in request.files:
        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.endswith(".xml"):
            return jsonify({"error": "Provided file is not XML."}), 400

        try:
            xml = file.read().decode("utf-8")
            response, status_code = report_service.import_from_xml(xml)
            return response, status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.data:
        try:
            xml = request.data.decode("utf-8")
            response, status_code = report_service.import_from_xml(xml)
            return response, status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No XML data provided."}), 400
