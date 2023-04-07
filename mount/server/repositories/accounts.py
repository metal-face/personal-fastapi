from typing import Any, Union
from uuid import UUID

from server.utils import services

READ_PARAMS = "account_id, username, email, role, created_at, updated_at"

async def create(account_id: UUID, username: str, email: str, password: str, role: str) -> dict[str, Any]:
    account = await services.database.fetch_one(
        query=f"""
            INSERT INTO accounts (account_id, username, email, password, role)
            VALUES (:account_id, :username, :email, :password, :role)
            RETURNING {READ_PARAMS}
        """,
        values={
            "account_id": account_id,
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        },
    )
    assert account is not None
    return dict(account._mapping)


async def fetch_many(page: int, page_size: int, role: str | None = None) -> list[dict[str, Any]]:
    accounts = await services.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS} 
            FROM accounts
            WHERE role = COALESCE(:role, role)
            LIMIT :limit
            OFFSET :offset
        """,
        values={
            "limit": page_size,
            "offset": (page - 1) * page_size,
            "role": role,
        },
    )
    return [dict(account._mapping) for account in accounts]


async def fetch_one(account_id: UUID) -> Union[dict[str, Any], None]:
    account = await services.database.fetch_one(
        query=f"""
            SELECT {READ_PARAMS} 
            FROM accounts 
            WHERE account_id = :account_id
        """,
        values={
            "account_id": account_id,
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
    account_id: UUID,
    username: str | None,
    email: str | None,
    password: str | None,
    role: str | None,
) -> dict[str, Any] | None:
    account = await services.database.fetch_one(
        query=f"""
            UPDATE accounts
            SET username = COALESCE(:username, username),
            email = COALESCE(:email, email),
            password = COALESCE(:password, password)
            role = COALESCE(:role, role)
            WHERE account_id = :account_id
            RETURNING {READ_PARAMS}
        """,
        values={
            "account_id": account_id,
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        },
    )
    return dict(account._mapping) if account is not None else None


async def delete_by_id(account_id: UUID) -> Union[dict[str, Any], None]:
    account = await services.database.fetch_one(
        query=f"""
            DELETE FROM accounts
            WHERE account_id = :account_id
            RETURNING {READ_PARAMS}
        """,
        values={
            "account_id": account_id,
        },
    )
    return dict(account._mapping) if account is not None else None
