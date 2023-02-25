from uuid import UUID
from datetime import datetime

from typing import TypedDict

class Account(TypedDict):
    id: UUID
    username: str
    email: str
    password: str
    created_at: datetime 
