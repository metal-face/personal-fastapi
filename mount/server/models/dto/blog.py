from pydantic import BaseModel
from uuid import UUID


class BlogDTO(BaseModel):
    blog_post: str
    blog_title: str
    account_id: UUID


class BlogUpdateDTO(BaseModel):
    blog_post: str
    blog_title: str
    account_id: UUID
