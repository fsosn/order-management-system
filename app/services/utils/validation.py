from app.model import Status
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
    errors.update(order_errors["errors"])

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

    if "name" in data:
        if not isinstance(data["name"], str):
            errors["name"] = "Name must be a string."
        elif len(data["name"]) > 128:
            errors["name"] = "Name must be maximum 128 characters long."

    if "description" in data:
        if not isinstance(data["description"], str):
            errors["description"] = "Description must be a string."
        elif len(data["description"]) > 256:
            errors["description"] = "Description must be maximum 256 characters long."

    if "creation_date" in data:
        try:
            datetime.strptime(data["creation_date"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            errors["creation_date"] = (
                "Invalid date format. Should be 'YYYY-MM-DD HH:MM:SS'."
            )

    if "status" in data:
        if not isinstance(data["status"], str):
            errors["status"] = "Status must be a string."
        else:
            try:
                Status(data["status"])
            except ValueError:
                errors["status"] = (
                    f"Invalid status value. Choose one of: {', '.join([s.value for s in Status])}"
                )

    return {"errors": errors}
