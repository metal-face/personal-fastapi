from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class Account(BaseModel):
    id: UUID
    username: str
    email: str
    password: str
    created_at: datetime
