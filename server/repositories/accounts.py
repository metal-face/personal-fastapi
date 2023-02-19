from typing import Any, Union
from uuid import UUID

from server import services

READ_PARAMS = "id, username, email, created_at"


async def create_account(username: str, email: str, password: str) -> dict[str, Any]:
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
    return dict(account._mapping)


async def get_all_accounts() -> list[dict[str, Any]]:
    accounts = await services.database.fetch_all(
        query=f"""
            SELECT {READ_PARAMS} 
            FROM accounts
        """,
    )
    return [dict(account) for account in accounts]


async def get_account_by_id(id: UUID) -> Union[dict[str, Any], None]:
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
    return dict(account) if account is not None else None
