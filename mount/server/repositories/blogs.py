from typing import Any, Union
from uuid import UUID

from server.utils import services

READ_PARAMS = "blog_id, blog_post, created_at, updated_at, created_by"


async def create(
    account_id: UUID,
    blog_id: UUID,
    blog_post: str,
) -> dict[str, Any]:
    blog = await services.database.fetch_one(
        query=f"""
            INSERT INTO blogs (blog_id, blog_post, account_id)
            VALUES (:blog_id, :blog_post, :account_id)
            RETURN {READ_PARAMS}
        """,
        values={
            "blog_id": blog_id,
            "blog_post": blog_post,
            "account_id": account_id,
        },
    )
    assert blog is not None
    return dict(blog._mapping)


async def fetch_many(
    page: int,
    page_size: int,
    account_id: UUID | None = None,
) -> list[dict[str, Any]]:
    blogs = await services.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS}
            FROM blogs
            WHERE account_id = COALESCE(:account_id, account_id)
            LIMIT :limit
            OFFSET :offset
        """,
        values={
            "limit": page_size,
            "offset": (page - 1) * page_size,
            "account_id": account_id,
        },
    )
    return [dict(blog._mapping) for blog in blogs]
