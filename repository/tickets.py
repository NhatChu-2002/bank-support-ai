from typing import Optional, Dict, Any
from datetime import datetime
import random

from db import get_conn

def generate_unique_ticket(conn) -> str:
    while True:
        ticket = f"{random.randint(0, 999999):06d}"
        row = conn.execute(
            "SELECT 1 FROM support_tickets WHERE ticket_number = ?",
            (ticket,),
        ).fetchone()
        if not row:
            return ticket

def insert_ticket(customer_name: Optional[str], message: str) -> str:
    conn = get_conn()
    ticket = generate_unique_ticket(conn)
    now = datetime.utcnow().isoformat()

    conn.execute(
        """
        INSERT INTO support_tickets (ticket_number, customer_name, message, status, created_at, updated_at)
        VALUES (?, ?, ?, 'unresolved', ?, ?)
        """,
        (ticket, customer_name, message, now, now),
    )
    conn.commit()
    conn.close()
    return ticket

def get_ticket(ticket_number: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    row = conn.execute(
        """
        SELECT ticket_number, customer_name, message, status, created_at, updated_at
        FROM support_tickets
        WHERE ticket_number = ?
        """,
        (ticket_number,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def update_ticket_status(ticket_number: str, status: str) -> bool:
    conn = get_conn()
    now = datetime.utcnow().isoformat()
    cur = conn.execute(
        "UPDATE support_tickets SET status = ?, updated_at = ? WHERE ticket_number = ?",
        (status, now, ticket_number),
    )
    conn.commit()
    conn.close()
    return cur.rowcount > 0
