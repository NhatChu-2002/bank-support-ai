from typing import Optional, Dict, Any
from db import get_conn

def log_interaction(
    customer_name: Optional[str],
    user_message: str,
    classification: Dict[str, Any],
    response_text: str,
    db_action: str = "none",
    db_ticket_number: Optional[str] = None,
) -> None:
    try:
        conn = get_conn()
        conn.execute(
            """
            INSERT INTO interaction_logs
            (customer_name, user_message, category, sentiment, extracted_ticket_number, response_text, db_action, db_ticket_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_name,
                user_message,
                classification.get("category"),
                classification.get("sentiment"),
                classification.get("ticket_number"),
                response_text,
                db_action,
                db_ticket_number,
            ),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass
