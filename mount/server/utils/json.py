from fastapi.responses import JSONResponse
from typing import Any
import orjson
from asyncpg.pgproto import pgproto
from uuid import UUID
from pydantic import BaseModel


def _default_processor(data: Any) -> Any:
    if isinstance(data, BaseModel):
        return _default_processor(data.dict())
    elif isinstance(data, dict):
        return {k: _default_processor(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_default_processor(v) for v in data]
    elif isinstance(data, (UUID, pgproto.UUID)):
        return str(data)
    else:
        return data


class OrJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, default=_default_processor)
