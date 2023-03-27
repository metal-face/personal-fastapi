from typing import Any, Union
from uuid import UUID

from server.utils import services

READ_PARAMS = "id, username, email, created_at"


async def create(username: str, email: str, password: str) -> dict[str, Any]:
    account = await services.database.fetch_one(
        query=f"""
            INSERT INTO accounts (username, email, password)
            VALUES (:username, :email, :password)
            RETURNING ({READ_PARAMS})
        """,
        values={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert account is not None
    return dict(account._mapping.items())


async def fetch_many(page: int, page_size: int) -> list[dict[str, Any]]:
    accounts = await services.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS} 
            FROM accounts
            LIMIT :limit
            OFFSET :offset
        """,
        values={
            "limit": page_size,
            "offset": (page - 1) * page_size,
        },
    )
    return [dict(account._mapping) for account in accounts]


async def fetch_one(id: UUID) -> Union[dict[str, Any], None]:
    account = await services.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS} 
            FROM accounts 
            WHERE id = :id
        """,
        values={
            "id": id,
        },
    )
    return dict(account._mapping) if account is not None else None


async def fetch_by_email(email: str) -> Union[dict[str, Any], None]:
    account = await services.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM accounts
            WHERE email = :email
        """,
        values={"email": email},
    )
    return dict(account._mapping) if account is not None else None


async def fetch_by_username(username: str) -> Union[dict[str, Any], None]:
    account = await services.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS}
            FROM accounts
            where username = :username
        """,
        values={"username": username},
    )
    return dict(account._mapping) if account is not None else None


async def update_by_id(
    id: UUID,
    username: str | None,
    email: str | None,
    password: str | None,
) -> dict[str, Any] | None:
    account = await services.database.fetch_one(
        query=f"""
            UPDATE accounts
            SET username = COALESCE(:username, username),
            email = COALESCE(:email, email),
            password = COALESCE(:password, password)
            WHERE id = :id
            RETURNING ({READ_PARAMS})
        """,
        values={
            "id": id,
            "username": username,
            "email": email,
            "password": password,
        },
    )
    return dict(account) if account is not None else None


async def delete_by_id(id: UUID) -> Union[dict[str, Any], None]:
    account = await services.database.fetch_one(
        query=f"""
            DELETE FROM accounts
            WHERE id = :id
            RETURNING ({READ_PARAMS})
        """,
        values={
            "id": id,
        },
    )
    return dict(account._mapping) if account is not None else None
