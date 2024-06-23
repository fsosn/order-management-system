from ...model import Status
from datetime import datetime


def validate_request_data(data):
    required_fields = ["name", "description"]
    errors = {}

    for field in required_fields:
        if field not in data:
            errors[field] = f"Field '{field}' is required."
        elif not isinstance(data[field], str) or not data[field].strip():
            errors[field] = f"Field '{field}' must be a non-empty string."

    order_errors = validate_order_data(data)
    errors.update(order_errors)

    return {"errors": errors}


def validate_order_data(data):
    errors = {}

    if "id" in data:
        try:
            id_value = int(data["id"])
            if id_value <= 0:
                errors["id"] = "ID must be a positive integer."
        except ValueError:
            errors["id"] = "ID must be an integer."

    if "name" in data and len(data["name"]) > 128:
        errors["name"] = "Name must be 128 characters or less."

    if "description" in data and len(data["description"]) > 256:
        errors["description"] = "Description must be 256 characters or less."

    if "creation_date" in data:
        try:
            datetime.strptime(data["creation_date"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            errors["creation_date"] = (
                "Invalid date format. Should be 'YYYY-MM-DD HH:MM:SS'."
            )

    status_values = [status.value for status in Status]
    if "status" in data and data["status"] not in status_values:
        errors["status"] = (
            f"Invalid status value. Choose one of: {', '.join(status_values)}"
        )

    return {"errors": errors}
