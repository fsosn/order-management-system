import xml.etree.ElementTree as ET
from app.model import Order
from app.extensions import db


def test_export_to_xml(client, init_orders):
    response = client.get("/api/orders/export/xml")
    assert response.status_code == 200

    xml = response.data
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()

    assert root.tag == "Orders"

    orders = Order.query.order_by(Order.id).all()
    assert len(root.findall("Order")) == len(orders)

    order_elements = root.findall("Order")
    for i, order in enumerate(orders):
        element = order_elements[i]
        assert element.find("ID").text == str(order.id)
        assert element.find("Name").text == order.name
        assert element.find("Description").text == order.description
        assert element.find("CreationDate").text == order.creation_date.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        assert element.find("Status").text == order.status.value


def test_import_from_xml_valid(client, init_orders):
    id = 4
    name = "Order4"
    description = "Description4"
    creation_date = "2024-06-22 11:11:11"
    status = "NEW"

    xml = f"""
    <Orders>
        <Order>
            <ID>{id}</ID>
            <Name>{name}</Name>
            <Description>{description}</Description>
            <CreationDate>{creation_date}</CreationDate>
            <Status>{status}</Status>
        </Order>
    </Orders>
    """

    response = client.post(
        "/api/orders/import/xml", data=xml, content_type="application/xml"
    )

    assert response.status_code == 200

    imported_order = db.session.get(Order, id)
    assert imported_order is not None
    assert imported_order.name == name
    assert imported_order.description == description
    assert imported_order.status.value == status
    assert imported_order.creation_date.strftime("%Y-%m-%d %H:%M:%S") == creation_date


def test_import_from_xml_invalid_format(client):
    xml = "<Orders><Order><ID>1</ID><Name>Test</Name><Description></Orders>"

    response = client.post(
        "/api/orders/import/xml", data=xml, content_type="application/xml"
    )

    assert response.status_code == 400


def test_import_from_xml_missing_elements(client):
    xml = """
    <Orders>
        <Order>
            <ID>1</ID>
            <Status>Test</Status>
        </Order>
    </Orders>
    """

    response = client.post(
        "/api/orders/import/xml",
        data=xml,
        content_type="application/xml",
    )

    assert response.status_code == 400


def test_import_from_xml_incorrect_data(client):
    xml = """
    <Orders>
        <Order>
            <ID>11</ID>
            <Name>Order</Name>
            <Description>Description</Description>
            <CreationDate>2024-06-23 15:15:15</CreationDate>
            <Status>TEST</Status>
        </Order>
    </Orders>
    """

    response = client.post(
        "/api/orders/import/xml",
        data=xml,
        content_type="application/xml",
    )

    assert response.status_code == 400
