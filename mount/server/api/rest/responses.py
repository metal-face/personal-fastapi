from typing import Any, TypeVar, TypedDict, Literal, Mapping, Iterable, Generic
from server.utils.json import OrJSONResponse
from server.utils.errors import ServiceError
from pydantic.generics import GenericModel
from pydantic import BaseModel
from fastapi import status, Response


T = TypeVar("T")


class Cookie(TypedDict, total=False):
    key: str
    value: str
    max_age: int | None
    expires: int | None
    path: str
    domain: str | None
    secure: bool
    httponly: bool
    samesite: Literal["lax", "strict", "none"]


def create_response(
    content: Mapping[str, Any],
    status_code: int,
    headers: dict[str, str] | None,
    cookies: Iterable[Cookie] | None = None,
) -> OrJSONResponse:
    response = OrJSONResponse(content, status_code, headers)

    if cookies is None:
        cookies = []

    for cookie in cookies:
        response.set_cookie(**cookie)

    return response


class Success(GenericModel, Generic[T]):
    status: Literal["success"]
    data: T
    
class Failure(BaseModel):
    status: Literal["failure"]
    error: ServiceError
    message: str
    

def format_success(data: Any) -> dict[str, Any]:
    return {"status": "success", "data": data}


def success(
    data: Any,
    status_code: int = 200,
    headers: dict | None = None,
    cookies: Iterable[Cookie] | None = None,
) -> Any:
    content = format_success(data)
    return create_response(content, status_code, headers, cookies)


def format_failure(error: ServiceError, message: str) -> dict[str, Any]:
    return {"status": "error", "error": error, "message": message}


def failure(
    error: ServiceError,
    message: str,
    headers: dict | None = None,
    cookies: Iterable[Cookie] | None = None,
    status_code: int = 400,
) -> Any:
    content = format_failure(error, message)
    return create_response(content, status_code, headers, cookies)

def no_content(headers: dict[str, Any] | None = None) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT, headers=headers)
