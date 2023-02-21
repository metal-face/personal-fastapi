import typing

from server.utils.errors import ServiceError
import server.utils.validation as validation
import server.repositories.accounts as repo
from server.repositories import accounts


async def signup(
    email_address: str,
    password: str,
    username: str,
) -> dict[str, typing.Any] | ServiceError:
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

    