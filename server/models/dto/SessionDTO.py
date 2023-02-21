from pydantic import BaseModel


class SessionDTO(BaseModel):
    username: str
    password: str
