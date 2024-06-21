from .model import Status


def validate_order(data):
    required_fields = ["name", "description"]
    errors = {}

    for field in required_fields:
        if field not in data:
            errors[field] = f"Field '{field}' is required."
        elif not isinstance(data[field], str) or not data[field].strip():
            errors[field] = f"Field '{field}' must be a non-empty string."

    if "name" in data and len(data["name"]) > 128:
        errors["name"] = "Name must be 128 characters or less."

    if "description" in data and len(data["description"]) > 256:
        errors["description"] = "Description must be 256 characters or less."

    status_values = [status.value for status in Status]
    if "status" in data and data["status"] not in status_values:
        errors["status"] = (
            f"Invalid status value. Choose one of: {', '.join(status_values)}"
        )

    return errors
