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


@orders_bp.route("/api/orders", methods=["PUT"])
def bulk_update_statuses():
    data = request.get_json()
    if not data or "id_list" not in data or "status" not in data:
        return (
            jsonify({"error": "Properties 'id_list' and 'status' are required."}),
            400,
        )

    id_list = data["id_list"]
    status = data["status"]

    response, status_code = order_service.bulk_update_statuses(id_list, status)
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


@orders_bp.route("/api/orders/export/hdf5", methods=["GET"])
def export_to_hdf5():
    hdf5 = report_service.export_to_hdf5()
    return send_file(
        hdf5,
        download_name="orders.h5",
        as_attachment=True,
        mimetype="application/x-hdf5",
    )


@orders_bp.route("/api/orders/import/hdf5", methods=["POST"])
def import_from_hdf5():
    if "file" in request.files:
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        if not file.filename.endswith(".h5"):
            return jsonify({"error": "Provided file is not HDF5."}), 400
        try:
            response, status_code = report_service.import_from_hdf5(file)
            return response, status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No HDF5 file provided."}), 400
