from typing import Any, Union
from uuid import UUID


from server.utils.errors import ServiceError
import server.utils.validation as validation
import server.repositories.accounts as repo
from server.repositories import accounts
# TODO: Check with Josh to see if the repository layer is returning the correct data format. Should it be returning None if no account is found at that id?
# TODO: In the appropriate methods below, Check for an empty array instead. The repository layer won't return None, it will return an empty array.1


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

    if await accounts.fetch_by_email(email=email_address) is not None:
        return ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS

    if await accounts.fetch_by_username(username=username) is not None:
        return ServiceError.ACCOUNTS_USERNAME_EXISTS

    account = await accounts.create(
        email=email_address,
        password=password,
        username=username,
    )

    if account is None:
        return ServiceError.ACCOUNTS_SIGNUP_FAILED

    return account


async def fetch_one(id: UUID) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.fetch_one(id)
    
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_by_email(email: str) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.fetch_by_email(email)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_by_username(username: str) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.fetch_by_username(username)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_many(page: int, page_size: int) -> Union[list[dict[str, Any]], ServiceError]:
    user_accounts = await accounts.fetch_many(page, page_size)
    
    if user_accounts is None:
        return ServiceError.ACCOUNTS_NOT_FOUND
    
    return user_accounts

async def update_by_id(
    id: UUID, 
    username: str | None = None, 
    email: str | None = None, 
    password: str | None = None,
) -> Union[dict[str, Any], ServiceError]:
    user_account = await accounts.update_by_id(id, username, email, password)
    
    if user_account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND
    
    return user_account
    

async def delete_by_id(id: UUID) -> Union[dict[str, Any], ServiceError]:
    account = await accounts.delete_by_id(id)
    
    if account is None:
        return ServiceError.ACCOUNTS_DELETION_FAILED
    
    return account
