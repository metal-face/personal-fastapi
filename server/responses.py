from typing import Any
from server.json import OrJSONResponse


def success(
    content: Any,
    status_code: int = 200,
    meta: dict[str, Any] = {},
):
    data = {
        "status": "success",
        "content": content,
        "meta": meta,
    }
    return OrJSONResponse(
        content=data,
        status_code=status_code,
    )


def failure(
    content: Any,
    status_code: int = 400,
):
    data = {
        "status": "error",
        "content": content,
    }
    return OrJSONResponse(
        content=data,
        status_code=status_code,
    )
