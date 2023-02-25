from __future__ import annotations


import json
import typing
from datetime import datetime
from datetime import timedelta
from uuid import UUID

SESSION_EXPIRY = 60 * 60 * 24 * 30


def make_key(session_id: UUID | typing.Literal["*"]) -> str:
    return f"server:sessions:{session_id}"


def serialize(session: typing.Mapping[str, typing.Any]) -> str:
    return json.dumps(
        {
            "session_id": str(session["session_id"]),
            "account_id": str(session["account_id"]),
            "user_agent": session["user_agent"],
            "expires_at": session["expires_at"].isoformat(),
        }
    )
