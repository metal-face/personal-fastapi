from uuid import UUID
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from server.services import accounts
from server.api.rest import responses
from server.utils.errors import ServiceError
from server.models.dto.accounts import AccountUpdateDTO
from server.models.dto.accounts import AccountDTO
from fastapi import status

router = APIRouter(tags=["Accounts"])


class Account(BaseModel):
    account_id: UUID
    username: str
    role: str
    created_at: datetime


def determine_status_code(error: ServiceError) -> int:
    match error:
        case ServiceError.ACCOUNTS_EMAIL_ADDRESS_INVALID:
            return status.HTTP_422_UNPROCESSABLE_ENTITY
        case ServiceError.ACCOUNTS_PASSWORD_INVALID:
            return status.HTTP_422_UNPROCESSABLE_ENTITY
        case ServiceError.ACCOUNTS_USERNAME_INVALID:
            return status.HTTP_422_UNPROCESSABLE_ENTITY
        case ServiceError.ACCOUNTS_USERNAME_EXISTS:
            return status.HTTP_409_CONFLICT
        case ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS:
            return status.HTTP_409_CONFLICT
        case ServiceError.ACCOUNTS_NOT_FOUND:
            return status.HTTP_404_NOT_FOUND
        case ServiceError.RECAPTCHA_VERIFICATION_FAILED:
            return status.HTTP_400_BAD_REQUEST
        case ServiceError.INTERNAL_SERVER_ERROR:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        case _:
            return status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post("/accounts")
async def create_account(args: AccountDTO):
    result = await accounts.signup(
        args.email, args.password, args.username, args.role, args.token
    )

    if isinstance(result, ServiceError):
        status_code = determine_status_code(result)
        if result is ServiceError.ACCOUNTS_SIGNUP_FAILED:
            return responses.failure(
                result, message="Signup Failed!", status_code=status_code
            )
        elif result is ServiceError.ACCOUNTS_PASSWORD_INVALID:
            return responses.failure(
                result, message="Password Invalid!", status_code=status_code
            )
        elif result is ServiceError.ACCOUNTS_EMAIL_ADDRESS_INVALID:
            return responses.failure(
                result, message="Email Invalid!", status_code=status_code
            )
        elif result is ServiceError.ACCOUNTS_USERNAME_INVALID:
            return responses.failure(
                result, message="Username Invalid!", status_code=status_code
            )
        elif result in ServiceError.ACCOUNTS_USERNAME_EXISTS:
            return responses.failure(
                result, message="Username exists!", status_code=status_code
            )
        elif result in ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS:
            return responses.failure(
                result, message="Email already exists!", status_code=status_code
            )
        elif result is ServiceError.RECAPTCHA_VERIFICATION_FAILED:
            return responses.failure(
                result,
                message="ReCaptcha Authentication Failed!",
                status_code=status_code,
            )
        else:
            return responses.failure(
                result,
                message="Error! Internal Server Error!",
                status_code=status_code,
            )

    resp = Account.model_validate(result)
    return responses.success(resp)


@router.get("/accounts")
async def fetch_many(page: int = 1, page_size: int = 30):
    result = await accounts.fetch_many(page, page_size)
    if isinstance(result, ServiceError):
        status_code = determine_status_code(result)
        return responses.failure(
            result,
            message="Error! Internal Server Error!",
            status_code=status_code,
        )

    if result is None:
        return responses.success(
            [],
            200,
            meta={
                "page": page,
                "page_size": page_size,
                "total": 0,
            },
        )

    total = await accounts.fetch_total_count()
    if isinstance(total, ServiceError):
        status_code = determine_status_code(total)
        return responses.failure(
            total,
            message="Error! Internal Server Error!",
            status_code=status_code,
        )

    return responses.success(
        data=[Account.model_validate(account) for account in result],
        status_code=200,
        meta={
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    )


@router.get("/accounts/{id}")
async def fetch_one(id: UUID):
    result = await accounts.fetch_one(id)

    if isinstance(result, ServiceError):
        return responses.failure(
            result,
            message="Account not found!",
            status_code=404,
        )
    resp = Account.model_validate(result)
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
        status_code = determine_status_code(result)
        if result == ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS:
            return responses.failure(
                result,
                message="An account with this email already exists!",
                status_code=status_code,
            )
        elif result == ServiceError.ACCOUNTS_USERNAME_EXISTS:
            return responses.failure(
                result,
                message="An account with this username already exists!",
                status_code=status_code,
            )
        else:
            return responses.failure(
                result,
                message="Account update failed!",
                status_code=status_code,
            )
    resp = Account.model_validate(result)
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

    resp = Account.model_validate(result)
    return responses.success(resp)
