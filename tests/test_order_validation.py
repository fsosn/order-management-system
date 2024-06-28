from app.services.utils.validation import validate_order_data, validate_request_data
from app.model import Status

common_data = {
    "id": "1",
    "name": "order name",
    "description": "order description",
    "creation_date": "2024-06-23 12:12:12",
    "status": Status.NEW.value,
}


def test_validate_order_data_valid():
    data = common_data.copy()
    errors = validate_order_data(data)
    assert not errors["errors"]


def test_validate_order_data_id_is_string():
    data = common_data.copy()
    data["id"] = "one"
    errors = validate_order_data(data)
    assert "id" in errors["errors"]


def test_validate_order_data_id_is_negative():
    data = common_data.copy()
    data["id"] = -1
    errors = validate_order_data(data)
    assert "id" in errors["errors"]


def test_validate_order_data_name_too_long():
    data = common_data.copy()
    data["name"] = "a" * 129
    errors = validate_order_data(data)
    assert "name" in errors["errors"]


def test_validate_order_data_description_length():
    data = common_data.copy()
    data["description"] = "a" * 257
    errors = validate_order_data(data)
    assert "description" in errors["errors"]


def test_validate_order_data_invalid_datetime_format():
    data = common_data.copy()
    data["creation_date"] = "2024/06/23 12:00:00"
    errors = validate_order_data(data)
    assert "creation_date" in errors["errors"]


def test_validate_order_data_invalid_status():
    data = common_data.copy()
    data["status"] = "TEST"
    errors = validate_order_data(data)
    assert "status" in errors["errors"]


def test_validate_request_data_missing_required_fields():
    data = common_data.copy()
    del data["name"]
    errors = validate_request_data(data)
    assert "name" in errors["errors"]

    data = common_data.copy()
    del data["description"]
    errors = validate_request_data(data)
    assert "description" in errors["errors"]


def test_validate_request_data_non_string_fields():
    data = common_data.copy()
    data["name"] = 123
    errors = validate_request_data(data)
    assert "name" in errors["errors"]

    data = common_data.copy()
    data["description"] = 123
    errors = validate_request_data(data)
    assert "description" in errors["errors"]
