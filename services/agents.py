from typing import Optional, Dict, Any
from repository.tickets import insert_ticket, get_ticket

def feedback_handler(category: str, customer_name: Optional[str], message: str) -> Dict[str, Any]:
    if category == "positive_feedback":
        name = customer_name or "there"
        return {"response": f"Thank you for your kind words, {name}! We’re delighted to assist you."}

    ticket = insert_ticket(customer_name, message)
    return {
        "ticket_number": ticket,
        "response": f"We apologize for the inconvenience. A new ticket #{ticket} has been created. Our support team will look into this promptly.",
    }

def query_handler(ticket_number: Optional[str]) -> Dict[str, Any]:
    if not ticket_number:
        return {"response": "Sure — please share your 6-digit ticket number and I’ll check the status."}

    ticket = get_ticket(ticket_number)
    if not ticket:
        return {"response": f"I couldn’t find ticket #{ticket_number}. Please double-check the number."}

    return {"response": f"Your ticket #{ticket_number} is currently marked as: {ticket['status']}."}
