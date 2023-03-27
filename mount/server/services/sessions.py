from uuid import UUID
from uuid import uuid4
from typing import Any, Union
from server.utils.errors import ServiceError
from server.utils.validation import validate_password
from server.repositories import accounts
from server.repositories import sessions


async def login(
    username: str,
    password: str,
    user_agent: str,
) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.fetch_by_username(username)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    if not validate_password(password):
        return ServiceError.CREDENTIALS_INCORRECT

    session_id = uuid4()
    session = await sessions.create(
        session_id=session_id,
        account_id=account["id"],
        user_agent=user_agent,
    )

    return session


async def fetch_one(session_id: UUID) -> Union[dict[str, Any], ServiceError]:
    session = await sessions.fetch_one(session_id)

    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    return session


async def fetch_many(
    account_id: int | None,
    user_agent: str | None,
    page: int,
    page_size: int,
) -> list[dict[str, Any]]:
    all_sessions = await sessions.fetch_many(
        account_id=account_id,
        user_agent=user_agent,
        page=page,
        page_size=page_size,
    )

    return all_sessions


async def logout(session_id: UUID) -> Union[dict[str, Any], ServiceError]:
    session = await sessions.fetch_one(session_id)

    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    await sessions.delete_session_by_id(session_id)

    return session
