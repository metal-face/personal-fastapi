from pydantic import BaseModel

class AccountDTO(BaseModel):
    username: str
    email: str
    password: str
