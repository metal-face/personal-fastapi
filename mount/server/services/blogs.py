from typing import Any, Union
from uuid import UUID, uuid4

from server.utils.errors import ServiceError
import server.utils.validation as validation
import server.repositories.accounts as repo
from server.repositories import blogs


async def create_post(
    account_id: UUID,
    blog_post: str,
    blog_title: str,
) -> Union[dict[str, Any], ServiceError]:
    if len(blog_post) < 100 | len(blog_post) > 200_000:
        return ServiceError.BLOG_POST_INCORRECT_LENGTH

    if len(blog_title) < 5 | len(blog_title) > 100:
        return ServiceError.BLOG_POST_TITLE_INCORRECT_LENGTH

    blog = await blogs.create(
        account_id=account_id,
        blog_id=uuid4(),
        blog_post=blog_post,
        blog_title=blog_title,
    )

    if blog is None:
        return ServiceError.BLOGS_CREATION_FAILED

    return blog


async def fetch_one(blog_id: UUID) -> Union[dict[str, Any], ServiceError]:
    blog = await blogs.fetch_one(blog_id)

    if blog is None:
        return ServiceError.BLOGS_POST_NOT_FOUND

    return blog


async def fetch_many(
    page: int, page_size: int, account_id: UUID | None = None
) -> Union[list[dict[str, Any]], ServiceError]:
    blog_posts = await blogs.fetch_many(page, page_size, account_id)

    return blog_posts


async def update_by_id(
    blog_id: UUID,
    blog_post: str,
    blog_title: str,
) -> Union[dict[str, Any], ServiceError]:
    if len(blog_post) < 100 | len(blog_post) > 200_000:
        return ServiceError.BLOG_POST_INCORRECT_LENGTH

    if len(blog_title) < 5 | len(blog_title) > 100:
        return ServiceError.BLOG_POST_TITLE_INCORRECT_LENGTH

    blog = await blogs.update_by_id(
        blog_id=blog_id,
        blog_post=blog_post,
        blog_title=blog_title,
    )

    if blog is None:
        return ServiceError.BLOGS_UPDATE_FAILED

    return blog


async def delete_by_id(blog_id: UUID) -> Union[dict[str, Any], ServiceError]:
    blog = await blogs.delete_by_id(blog_id)

    if blog is None:
        return ServiceError.BLOGS_DELETION_FAILED

    return blog
