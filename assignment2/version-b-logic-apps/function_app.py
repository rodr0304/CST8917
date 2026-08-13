import json
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

VALID_CATEGORIES = {
    "travel",
    "meals",
    "supplies",
    "equipment",
    "software",
    "other",
}


@app.route(route="validate-expense", methods=["POST"])
def validate_expense(req: func.HttpRequest) -> func.HttpResponse:
    try:
        expense = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({
                "valid": False,
                "message": "Request body must contain valid JSON."
            }),
            status_code=400,
            mimetype="application/json"
        )

    required_fields = [
        "employeeName",
        "employeeEmail",
        "amount",
        "category",
        "description",
        "managerEmail",
    ]

    missing_fields = []

    for field in required_fields:
        if field not in expense:
            missing_fields.append(field)
        elif expense[field] is None:
            missing_fields.append(field)
        elif isinstance(expense[field], str) and not expense[field].strip():
            missing_fields.append(field)

    if missing_fields:
        return func.HttpResponse(
            json.dumps({
                "valid": False,
                "message": "Missing required fields: " + ", ".join(missing_fields)
            }),
            status_code=200,
            mimetype="application/json"
        )

    category = str(expense["category"]).strip().lower()

    if category not in VALID_CATEGORIES:
        return func.HttpResponse(
            json.dumps({
                "valid": False,
                "message": (
                    "Invalid category. Valid categories are: "
                    + ", ".join(sorted(VALID_CATEGORIES))
                )
            }),
            status_code=200,
            mimetype="application/json"
        )

    try:
        amount = float(expense["amount"])
    except (TypeError, ValueError):
        return func.HttpResponse(
            json.dumps({
                "valid": False,
                "message": "Amount must be numeric."
            }),
            status_code=200,
            mimetype="application/json"
        )

    if amount < 0:
        return func.HttpResponse(
            json.dumps({
                "valid": False,
                "message": "Amount cannot be negative."
            }),
            status_code=200,
            mimetype="application/json"
        )

    normalized_expense = {
        "employeeName": str(expense["employeeName"]).strip(),
        "employeeEmail": str(expense["employeeEmail"]).strip().lower(),
        "amount": amount,
        "category": category,
        "description": str(expense["description"]).strip(),
        "managerEmail": str(expense["managerEmail"]).strip().lower(),
    }

    return func.HttpResponse(
        json.dumps({
            "valid": True,
            "message": "Expense validation successful.",
            "expense": normalized_expense
        }),
        status_code=200,
        mimetype="application/json"
    )
