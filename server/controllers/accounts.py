from fastapi import APIRouter, Response
from server.models.dto.AccountDTO import AccountDTO
from server.repositories import accounts
from uuid import UUID
from server import responses

router = APIRouter()


@router.post("/accounts")
async def create_account(args: AccountDTO):
    account = await accounts.create_account(args.username, args.email, args.password)
    return responses.success(account)


@router.get("/accounts")
async def get_all_accounts():
    user_accounts = await accounts.get_all_accounts()
    return responses.success(user_accounts)


@router.get("/accounts/{id}")
async def get_account_by_id(id: UUID):
    user_account = await accounts.get_account_by_id(id)

    if user_account is None:
        return responses.failure(user_account, status_code=404)

    return responses.success(user_account)
