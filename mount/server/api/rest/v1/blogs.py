from fastapi import APIRouter
from uuid import UUID
from server.models.dto.blog import BlogDTO
from server.models.dto.blog import BlogUpdateDTO
from server.services import blogs
from server.api.rest import responses
from server.utils.errors import ServiceError
from fastapi import Depends
from server.api.rest.authorization import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter(tags=["Blogs"])
http_scheme = HTTPBearer(auto_error=True)


@router.post("/blogs")
async def create_post(
    args: BlogDTO,
    http_credentials: HTTPAuthorizationCredentials | None = Depends(http_scheme),
):
    result = await blogs.create_post(
        args.account_id, args.blog_post, args.blog_title, http_credentials.credentials
    )

    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Blog post creation failed!",
            status_code=404,
        )

    return responses.success(result)


@router.get("/blogs")
async def fetch_many(
    page: int = 1,
    page_size: int = 30,
    account_id: UUID | None = None,
):
    result = await blogs.fetch_many(
        page=page,
        page_size=page_size,
        account_id=account_id,
    )

    if isinstance(result, ServiceError):
        return responses.failure(result, message="No Blogs Found!", status_code=404)

    return responses.success(result)


@router.get("/blogs/{blog_id}")
async def fetch_one(blog_id: UUID):
    result = await blogs.fetch_one(blog_id)

    if isinstance(result, ServiceError):
        return responses.failure(result, message="Blog not found!", status_code=404)

    return responses.success(result)


@router.patch("/blogs/{blog_id}")
async def update_by_id(
    blog_id: UUID,
    args: BlogUpdateDTO,
    http_credentials: HTTPAuthorizationCredentials | None = Depends(http_scheme),
):
    result = await blogs.update_by_id(
        blog_id=blog_id,
        blog_post=args.blog_post,
        blog_title=args.blog_title,
        session_id=http_credentials.credentials,
    )

    if isinstance(result, ServiceError):
        return responses.failure(result, message="Blog update failed!", status_code=400)

    return responses.success(result)


@router.delete("/blogs/{blog_id}")
async def delete_by_id(
    blog_id: UUID,
    http_credentials: HTTPAuthorizationCredentials | None = Depends(http_scheme),
):
    result = await blogs.delete_by_id(
        blog_id,
        http_credentials.credentials,
    )

    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Blog deletion failed",
            status_code=404,
        )

    return responses.success(result)
