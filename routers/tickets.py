from fastapi import APIRouter, HTTPException
from schemas import TicketStatusUpdate
from repository.tickets import update_ticket_status

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.patch("/{ticket_number}")
def set_ticket_status(ticket_number: str, payload: TicketStatusUpdate):
    status = payload.status.strip().lower()
    if status not in ("unresolved", "in_progress", "resolved"):
        raise HTTPException(status_code=400, detail="status must be: unresolved | in_progress | resolved")

    ok = update_ticket_status(ticket_number, status)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"ticket_number": ticket_number, "status": status}
