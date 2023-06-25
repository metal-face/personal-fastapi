from uuid import UUID
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from server.services import accounts
from server.api.rest import responses
from server.utils.errors import ServiceError
from server.models.dto.accounts import AccountUpdateDTO
from server.models.dto.accounts import AccountDTO

router = APIRouter(tags=["Accounts"])


class EmailRequest(BaseModel):
    email: str


class Account(BaseModel):
    account_id: UUID
    username: str
    role: str
    created_at: datetime


@router.post("/accounts")
async def create_account(args: AccountDTO):
    result = await accounts.signup(
        args.email,
        args.password,
        args.username,
        args.role,
    )

    if isinstance(result, ServiceError):
        if result is ServiceError.ACCOUNTS_SIGNUP_FAILED:
            return responses.failure(result, message="Signup Failed!", status_code=500)
        else:
            return responses.failure(
                result,
                message="Error! Internal Server Error!",
                status_code=500,
            )

    resp = Account.parse_obj(result)
    return responses.success(resp)


@router.post("/search")
async def fetch_by_email(request: EmailRequest):
    result = await accounts.fetch_by_email(request.email)

    if isinstance(result, ServiceError):
        if result is ServiceError.DATABASE_QUERY_FAILED:
            return responses.failure(
                result,
                message="Error! Internal Server Error!",
                status_code=500,
            )
    elif result is None:
        return responses.success(data=[])
    else:
        resp = Account.parse_obj(result)
        return responses.success(resp)


@router.get("/accounts")
async def fetch_many(page: int = 1, page_size: int = 30):
    result = await accounts.fetch_many(page, page_size)
    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Error! Internal Server Error!",
            status_code=500,
        )

    if result is None:
        return responses.success([])

    return responses.success([Account.parse_obj(account) for account in result])


@router.get("/accounts/{id}")
async def fetch_one(id: UUID):
    result = await accounts.fetch_one(id)

    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Account not found!",
            status_code=404,
        )
    resp = Account.parse_obj(result)
    return responses.success(resp)


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
    resp = Account.parse_obj(result)
    return responses.success(resp)


@router.delete("/accounts/{id}")
async def delete_by_id(id: UUID):
    result = await accounts.delete_by_id(id)

    if isinstance(result, ServiceError):
        if result is ServiceError.ACCOUNTS_DELETION_FAILED:
            return responses.failure(
                result,
                message="Account deletion failed!",
                status_code=500,
            )

    resp = Account.parse_obj(result)
    return responses.success(resp)
