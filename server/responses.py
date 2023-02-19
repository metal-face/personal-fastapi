from typing import Any
from fastapi.responses import JSONResponse


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
    return JSONResponse(
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
    return JSONResponse(
        content=data,
        status_code=status_code,
    )
