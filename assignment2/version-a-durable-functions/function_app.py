import azure.functions as func
import azure.durable_functions as df
import logging
from datetime import timedelta

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

VALID_CATEGORIES = [
    "travel",
    "meals",
    "supplies",
    "equipment",
    "software",
    "other",
]


# ============================================================
# HTTP CLIENT - START EXPENSE WORKFLOW
# ============================================================

@app.route(route="expenses/start", methods=["POST"])
@app.durable_client_input(client_name="client")
async def start_expense(
    req: func.HttpRequest,
    client: df.DurableOrchestrationClient
) -> func.HttpResponse:

    try:
        expense = req.get_json()
    except ValueError:
        return func.HttpResponse(
            '{"error": "Request body must contain valid JSON."}',
            status_code=400,
            mimetype="application/json"
        )

    instance_id = await client.start_new(
        "expense_orchestrator",
        None,
        expense
    )

    logging.info(
        "Started expense workflow with instance ID: %s",
        instance_id
    )

    return client.create_check_status_response(
        req,
        instance_id
    )


# ============================================================
# ORCHESTRATOR
# ============================================================

@app.orchestration_trigger(context_name="context")
def expense_orchestrator(
    context: df.DurableOrchestrationContext
):

    expense = context.get_input()

    # --------------------------------------------------------
    # STEP 1 - VALIDATION
    # --------------------------------------------------------

    validation = yield context.call_activity(
        "validate_expense",
        expense
    )

    if not validation["valid"]:
        return {
            "status": "validation_error",
            "message": validation["message"],
            "expense": expense
        }

    # --------------------------------------------------------
    # STEP 2 - PROCESS EXPENSE
    # --------------------------------------------------------

    processed_expense = yield context.call_activity(
        "process_expense",
        expense
    )

    amount = float(processed_expense["amount"])

    # --------------------------------------------------------
    # STEP 3A - AUTO APPROVAL UNDER $100
    # --------------------------------------------------------

    if amount < 100:

        result = {
            "status": "approved",
            "approvalType": "automatic",
            "escalated": False,
            "message": "Expense automatically approved because amount is under $100.",
            "expense": processed_expense
        }

        notification = yield context.call_activity(
            "send_notification",
            result
        )

        result["notification"] = notification

        return result

    # --------------------------------------------------------
    # STEP 3B - HUMAN INTERACTION
    # Expenses >= $100 wait for manager decision.
    #
    # Assignment demo timeout:
    # 60 seconds so the timeout scenario can be demonstrated.
    # --------------------------------------------------------

    timeout_seconds = 60

    deadline = (
        context.current_utc_datetime
        + timedelta(seconds=timeout_seconds)
    )

    manager_event = context.wait_for_external_event(
        "ManagerDecision"
    )

    timeout_task = context.create_timer(deadline)

    winner = yield context.task_any(
        [manager_event, timeout_task]
    )

    # --------------------------------------------------------
    # MANAGER RESPONDED
    # --------------------------------------------------------

    if winner == manager_event:

        if not timeout_task.is_completed:
            timeout_task.cancel()

        approved = manager_event.result

        # Normalize the external event payload returned by Durable Functions.
        if isinstance(approved, dict):
            approved = approved.get("decision", approved.get("approved"))

        approved_text = str(approved).strip().lower()

        if approved is True or approved_text in ("true", "approve", "approved"):
            result = {
                "status": "approved",
                "approvalType": "manager",
                "escalated": False,
                "message": "Expense approved by manager.",
                "expense": processed_expense
            }

        else:
            result = {
                "status": "rejected",
                "approvalType": "manager",
                "escalated": False,
                "message": "Expense rejected by manager.",
                "expense": processed_expense
            }

    # --------------------------------------------------------
    # TIMEOUT - AUTO APPROVE AND ESCALATE
    # --------------------------------------------------------

    else:

        result = {
            "status": "escalated",
            "approvalType": "timeout",
            "escalated": True,
            "message": (
                "Manager did not respond before the timeout. "
                "Expense automatically approved and flagged as escalated."
            ),
            "expense": processed_expense
        }

    # --------------------------------------------------------
    # STEP 4 - NOTIFICATION
    # --------------------------------------------------------

    notification = yield context.call_activity(
        "send_notification",
        result
    )

    result["notification"] = notification

    return result


# ============================================================
# ACTIVITY - VALIDATE EXPENSE
# ============================================================

@app.activity_trigger(input_name="expense")
def validate_expense(expense: dict):

    required_fields = [
        "employeeName",
        "employeeEmail",
        "amount",
        "category",
        "description",
        "managerEmail",
    ]

    if not isinstance(expense, dict):
        return {
            "valid": False,
            "message": "Expense must be a JSON object."
        }

    missing_fields = []

    for field in required_fields:

        if field not in expense:
            missing_fields.append(field)

        elif expense[field] is None:
            missing_fields.append(field)

        elif isinstance(expense[field], str) and not expense[field].strip():
            missing_fields.append(field)

    if missing_fields:

        return {
            "valid": False,
            "message": (
                "Missing required fields: "
                + ", ".join(missing_fields)
            )
        }

    category = str(
        expense.get("category", "")
    ).lower().strip()

    if category not in VALID_CATEGORIES:

        return {
            "valid": False,
            "message": (
                "Invalid category. Valid categories are: "
                + ", ".join(VALID_CATEGORIES)
            )
        }

    try:
        amount = float(expense["amount"])

        if amount < 0:
            return {
                "valid": False,
                "message": "Amount cannot be negative."
            }

    except (ValueError, TypeError):

        return {
            "valid": False,
            "message": "Amount must be numeric."
        }

    return {
        "valid": True,
        "message": "Expense validation successful."
    }


# ============================================================
# ACTIVITY - PROCESS EXPENSE
# ============================================================

@app.activity_trigger(input_name="expense")
def process_expense(expense: dict):

    processed = dict(expense)

    processed["employeeName"] = str(
        processed["employeeName"]
    ).strip()

    processed["employeeEmail"] = str(
        processed["employeeEmail"]
    ).strip().lower()

    processed["managerEmail"] = str(
        processed["managerEmail"]
    ).strip().lower()

    processed["category"] = str(
        processed["category"]
    ).strip().lower()

    processed["description"] = str(
        processed["description"]
    ).strip()

    processed["amount"] = float(
        processed["amount"]
    )

    return processed


# ============================================================
# ACTIVITY - SEND NOTIFICATION
# ============================================================

@app.activity_trigger(input_name="result")
def send_notification(result: dict):

    expense = result.get("expense", {})

    employee_email = expense.get(
        "employeeEmail",
        "unknown"
    )

    status = result.get(
        "status",
        "unknown"
    )

    logging.info(
        "Notification for %s - Expense status: %s",
        employee_email,
        status
    )

    # Version A simulates email delivery.
    # Version B will send the actual email through Logic Apps.

    return {
        "sent": True,
        "recipient": employee_email,
        "subject": f"Expense request: {status.upper()}",
        "deliveryMode": "simulated"
    }


# ============================================================
# HTTP CLIENT - MANAGER APPROVE / REJECT
# ============================================================

@app.route(
    route="expenses/{instanceId}/decision",
    methods=["POST"]
)
@app.durable_client_input(client_name="client")
async def manager_decision(
    req: func.HttpRequest,
    client: df.DurableOrchestrationClient
) -> func.HttpResponse:

    instance_id = req.route_params.get(
        "instanceId"
    )

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            '{"error": "Request body must contain valid JSON."}',
            status_code=400,
            mimetype="application/json"
        )

    decision = str(
        body.get("decision", "")
    ).lower().strip()

    if decision not in ["approve", "reject"]:

        return func.HttpResponse(
            '{"error": "Decision must be approve or reject."}',
            status_code=400,
            mimetype="application/json"
        )

    status = await client.get_status(instance_id)

    if status is None:
        return func.HttpResponse(
            '{"error": "Orchestration instance not found."}',
            status_code=404,
            mimetype="application/json"
        )

    approved = decision == "approve"

    await client.raise_event(
        instance_id,
        "ManagerDecision",
        approved
    )

    return func.HttpResponse(
        (
            "{"
            f'"instanceId": "{instance_id}",'
            f'"decision": "{decision}",'
            '"message": "Manager decision submitted successfully."'
            "}"
        ),
        status_code=202,
        mimetype="application/json"
    )


# ============================================================
# HTTP CLIENT - GET WORKFLOW STATUS
# ============================================================

@app.route(
    route="expenses/{instanceId}/status",
    methods=["GET"]
)
@app.durable_client_input(client_name="client")
async def expense_status(
    req: func.HttpRequest,
    client: df.DurableOrchestrationClient
) -> func.HttpResponse:

    instance_id = req.route_params.get(
        "instanceId"
    )

    status = await client.get_status(instance_id)

    if status is None:
        return func.HttpResponse(
            '{"error": "Orchestration instance not found."}',
            status_code=404,
            mimetype="application/json"
        )

    response = {
        "instanceId": instance_id,
        "runtimeStatus": str(status.runtime_status),
        "output": status.output
    }

    return func.HttpResponse(
        df.json.dumps(response),
        status_code=200,
        mimetype="application/json"
    )