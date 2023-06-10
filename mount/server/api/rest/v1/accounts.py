from fastapi import APIRouter, Request
from server.models.dto.accounts import AccountDTO
from server.services import accounts
from uuid import UUID
from server.api.rest import responses
from server.models.dto.accounts import AccountUpdateDTO
from server.utils.errors import ServiceError

router = APIRouter(tags=["Accounts"])


@router.post("/accounts")
async def create_account(args: AccountDTO):
    result = await accounts.signup(
        args.email,
        args.password,
        args.username,
        args.role,
    )

    if isinstance(result, ServiceError):
        return responses.failure(result, message="Signup Failed!", status_code=404)

    return responses.success(result)


@router.get("/accounts")
async def fetch_by_email(email: str, request: Request):
    result = await accounts.fetch_by_email(email)

    if isinstance(result, ServiceError):
        if result is ServiceError.DATABASE_QUERY_FAILED:
            return responses.failure(
                result,
                message="Error! Internal Server Error!",
                status_code=500,
            )
        elif result is ServiceError.ACCOUNTS_NOT_FOUND:
            return responses.success([])
    else:
        return responses.success(result)


@router.get("/accounts")
async def fetch_many(page: int = 1, page_size: int = 30):
    result = await accounts.fetch_many(page, page_size)
    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Error! Internal Server Error!",
            status_code=500,
        )

    return None if result is None else result


@router.get("/accounts/{id}")
async def fetch_one(id: UUID):
    result = await accounts.fetch_one(id)

    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Account not found!",
            status_code=404,
        )

    return responses.success(result)


@router.patch("/accounts/{id}")
async def update_by_id(id: UUID, args: AccountUpdateDTO):
    result = await accounts.update_by_id(
        id=id,
        username=args.username,
        email=args.email,
        password=args.password,
        role=args.role,
    )

    if isinstance(result, ServiceError):
        if result == ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS:
            return responses.failure(
                result,
                message="An account with this email already exists!",
                status_code=409,
            )
        elif result == ServiceError.ACCOUNTS_USERNAME_EXISTS:
            return responses.failure(
                result,
                message="An account with this username already exists!",
                status_code=409,
            )
        else:
            return responses.failure(
                result,
                message="Account update failed!",
                status_code=404,
            )

    return responses.success(result)


@router.delete("/accounts/{id}")
async def delete_by_id(id: UUID):
    result = await accounts.delete_by_id(id)

    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Account deletion failed!",
            status_code=404,
        )

    return responses.success(result)
