from fastapi import APIRouter
from server.models.dto.AccountDTO import AccountDTO
from server.repositories import accounts
from uuid import UUID
from server.api.rest import responses
from server.models.dto.AccountDTO import AccountUpdateDTO

router = APIRouter()


@router.post("/accounts")
async def create_account(args: AccountDTO):
    account = await accounts.create_account(args.username, args.email, args.password)
    return responses.success(account)


@router.get("/accounts")
async def get_many_accounts(page: int = 1, page_size: int = 30):
    user_accounts = await accounts.get_many_accounts(page, page_size)
    return responses.success(user_accounts)


@router.get("/accounts/{id}")
async def get_account_by_id(id: UUID):
    user_account = await accounts.get_account_by_id(id)

    if user_account is None:
        return responses.failure(user_account, status_code=404)

    return responses.success(user_account)


@router.patch("/accounts/{id}")
async def update_account_by_id(id: UUID, args: AccountUpdateDTO):
    user_account = await accounts.update_account_by_id(
        id=id,
        username=args.username,
        email=args.email,
        password=args.password,
    )

    if user_account is None:
        return responses.failure(user_account, status_code=404)

    return responses.success(user_account)


@router.delete("/accounts/{id}")
async def delete_account_by_id(id: UUID):
    user_account = await accounts.delete_account_by_id(id)

    if user_account is None:
        return responses.failure(user_account, status_code=404)

    return responses.success(user_account)
