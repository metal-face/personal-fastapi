from fastapi import Request


async def create_account(username: str, email: str, password: str, request: Request):
    create_account_statement = "INSERT INTO accounts (username, email, password) VALUES (:username, :email, :password)"

    create_params = {"username": username, "email": email, "password": password}

    row_id_returned = request.app.state.database.execute(
        create_account_statement, create_params
    )

    account_info_params = {"id": row_id_returned}

    account_info = (
        "SELECT id, username, email, password, created_at FROM accounts WHERE :id"
    )

    return request.app.state.database.fetch_one(account_info, account_info_params)
