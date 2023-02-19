from pydantic import BaseModel


class AccountDTO(BaseModel):
    username: str
    email: str
    password: str


class AccountUpdateDTO(BaseModel):
    username: str | None
    email: str | None
    password: str | None
