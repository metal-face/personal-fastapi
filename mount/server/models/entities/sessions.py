from datetime import datetime
from uuid import UUID

from . import BaseModel


class Session(BaseModel):
    session_id: UUID
    account_id: UUID
    user_agent: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
