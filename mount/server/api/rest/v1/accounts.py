from fastapi import APIRouter
from server.models.dto.accounts import AccountDTO
from server.services import accounts
from uuid import UUID
from server.api.rest import responses
from server.models.dto.accounts import AccountUpdateDTO
from server.utils.errors import ServiceError

router = APIRouter(tags=["Accounts"])


@router.post("/accounts")
async def create_account(args: AccountDTO):
    account = await accounts.signup(
        args.email,
        args.password,
        args.username,
        args.role,
    )

    if isinstance(account, ServiceError):
        return responses.failure(account, message="Signup Failed!", status_code=404)

    return responses.success(account)


@router.get("/accounts")
async def fetch_many(page: int = 1, page_size: int = 30):
    user_accounts = await accounts.fetch_many(page, page_size)

    if isinstance(user_accounts, ServiceError):
        return responses.failure(
            user_accounts, message="No Account Found!", status_code=404
        )

    return responses.success(user_accounts)


@router.get("/accounts/{id}")
async def fetch_one(id: UUID):
    user_account = await accounts.fetch_one(id)

    if isinstance(user_account, ServiceError):
        return responses.failure(
            user_account,
            message="Account not found!",
            status_code=404,
        )

    return responses.success(user_account)


@router.patch("/accounts/{id}")
async def update_by_id(id: UUID, args: AccountUpdateDTO):
    user_account = await accounts.update_by_id(
        id=id,
        username=args.username,
        email=args.email,
        password=args.password,
        role=args.role,
    )

    if isinstance(user_account, ServiceError):
        return responses.failure(
            user_account,
            message="Account update failed!",
            status_code=404,
        )

    return responses.success(user_account)


@router.delete("/accounts/{id}")
async def delete_by_id(id: UUID):
    user_account = await accounts.delete_by_id(id)

    if isinstance(user_account, ServiceError):
        return responses.failure(
            user_account,
            message="Account deletion failed!",
            status_code=404,
        )

    return responses.success(user_account)
