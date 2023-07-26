from pydantic import BaseModel
from enum import Enum


class RoleEnum(str, Enum):
    REGULAR = "REGULAR"
    SUPER = "SUPER"
    ADMIN = "ADMIN"


class AccountDTO(BaseModel):
    username: str
    email: str
    password: str
    role: RoleEnum
    token: str


class AccountUpdateDTO(BaseModel):
    username: str | None
    email: str | None
    password: str | None
    role: RoleEnum | None
