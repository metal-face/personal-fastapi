from typing import Any

from server import services

READ_PARAMS = "id, username, email, created_at"


async def create_account(username: str, email: str, password: str) -> dict[str, Any]:
    account = await services.database.execute(
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
    return account
