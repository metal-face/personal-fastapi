from __future__ import annotations


import json
from typing import Any, Union, Literal, Mapping
from datetime import datetime
from datetime import timedelta
from uuid import UUID
from server.utils import services


SESSION_EXPIRY = 60 * 60 * 24 * 30


def make_key(session_id: UUID | Literal["*"]) -> str:
    return f"server:sessions:{session_id}"


def serialize(session: Mapping[str, Any]) -> str:
    return json.dumps(
        {
            "session_id": str(session["session_id"]),
            "account_id": str(session["account_id"]),
            "user_agent": session["user_agent"],
            "expires_at": session["expires_at"].isoformat(),
            "created_at": session["created_at"].isoformat(),
            "updated_at": session["updated_at"].isoformat(),
        }
    )


def deserialize(raw_session: str) -> dict[str, Any]:
    session = json.loads(raw_session)

    assert isinstance(session, dict)

    session["session_id"] = UUID(session["session_id"])
    session["account_id"] = UUID(session["account_id"])
    session["expires_at"] = datetime.fromisoformat(session["expires_at"])
    session["created_at"] = datetime.fromisoformat(session["created_at"])
    session["updated_at"] = datetime.fromisoformat(session["updated_at"])

    return session


async def create(
    session_id: UUID,
    account_id: UUID,
    user_agent: str,
) -> dict[str, Any]:
    now = datetime.now()
    expires_at = now + timedelta(seconds=SESSION_EXPIRY)
    session = {
        "session_id": session_id,
        "account_id": account_id,
        "user_agent": user_agent,
        "expires_at": expires_at,
        "created_at": now,
        "updated_at": now,
    }

    await services.redis.set(name=make_key(session_id), value=serialize(session), ex=SESSION_EXPIRY)

    return session


async def fetch_one(session_id: UUID) -> Union[dict[str, Any], None]:
    session_key = make_key(session_id)
    session = await services.redis.get(session_key)
    return deserialize(session) if session is not None else None


async def fetch_many(
    account_id: UUID | None,
    user_agent: str | None,
    page: int,
    page_size: int,
) -> list[dict[str, Any]]:
    session_key = make_key("*")

    if page > 1:
        cursor, keys = await services.redis.scan(
            cursor=0,
            match=session_key,
            count=(page - 1) * page_size,
        )
    else:
        cursor = None

    sessions = []

    while cursor != 0:
        cursor, keys = await services.redis.scan(
            cursor=cursor or 0,
            match=session_key,
            count=page_size,
        )

        raw_sessions = await services.redis.mget(keys)

        for raw_session in raw_sessions:
            session = deserialize(raw_session)

            if account_id is not None and session["account_id"] != account_id:
                continue

            if user_agent is not None and session["user_agent"] != user_agent:
                continue

            sessions.append(session)

    return sessions


async def delete_session_by_id(session_id: UUID) -> Union[dict[str, Any], None]:
    session_key = make_key(session_id)

    session = await services.redis.get(session_key)
    if session is None:
        return None

    await services.redis.delete(session_key)
    return deserialize(session)
