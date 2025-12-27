from fastapi import APIRouter
from schemas import UserMessage
from services.classifier import classify
from services.agents import feedback_handler, query_handler
from repository.logs import log_interaction

router = APIRouter(tags=["chat"])

@router.post("/chat")
def chat(payload: UserMessage):
    classification = classify(payload.message)
    category = classification["category"]
    ticket_number = classification.get("ticket_number")

    if category in ("positive_feedback", "negative_feedback"):
        result = feedback_handler(category, payload.customer_name, payload.message)
        response_text = result["response"]

        db_action = "insert_ticket" if category == "negative_feedback" else "none"
        db_ticket_number = result.get("ticket_number")

        log_interaction(
            payload.customer_name,
            payload.message,
            classification,
            response_text,
            db_action=db_action,
            db_ticket_number=db_ticket_number,
        )

        return {"category": category, "classification": classification, **result}

    result = query_handler(ticket_number)
    response_text = result["response"]

    log_interaction(
        payload.customer_name,
        payload.message,
        classification,
        response_text,
        db_action=("select_ticket" if ticket_number else "none"),
        db_ticket_number=ticket_number,
    )

    return {"category": category, "classification": classification, **result}
