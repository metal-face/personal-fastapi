from typing import Any, Union
from uuid import UUID


from server.utils.errors import ServiceError
import server.utils.validation as validation
import server.repositories.accounts as repo
from server.repositories import accounts


async def signup(
    email_address: str,
    password: str,
    username: str,
) -> Union[dict[str, Any], ServiceError]:
    if not validation.validate_username(username):
        return ServiceError.ACCOUNTS_USERNAME_INVALID

    if not validation.validate_email(email_address):
        return ServiceError.ACCOUNTS_EMAIL_ADDRESS_INVALID

    if not validation.validate_password(password):
        return ServiceError.ACCOUNTS_PASSWORD_INVALID

    if await accounts.get_account_by_email(email=email_address) is not None:
        return ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS

    if await accounts.get_account_by_username(username=username) is not None:
        return ServiceError.ACCOUNTS_USERNAME_EXISTS

    account = await accounts.create_account(
        email=email_address,
        password=password,
        username=username,
    )

    if account is None:
        return ServiceError.ACCOUNTS_SIGNUP_FAILED

    return account


async def get_account_by_id(id: UUID) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.get_account_by_id(id)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def get_account_by_email(email: str) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.get_account_by_email(email)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def get_account_by_username(username: str) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.get_account_by_username(username)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_many_accounts(page: int, page_size: int) -> Union[list[dict[str, Any]], ServiceError]:
    user_accounts = await accounts.get_many_accounts(page, page_size)
    
    if user_accounts is None:
        return ServiceError.ACCOUNTS_NOT_FOUND
    
    return user_accounts
