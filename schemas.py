from pydantic import BaseModel
from typing import Optional

class UserMessage(BaseModel):
    customer_name: Optional[str] = None
    message: str

class TicketStatusUpdate(BaseModel):
    status: str  # unresolved | in_progress | resolved
