from typing import Any, Union
from uuid import UUID, uuid4
from server.utils import security
from server.utils.errors import ServiceError
from server.repositories import accounts
import server.utils.validation as validation
from server.adapters import recaptcha


async def signup(
    email_address: str, password: str, username: str, role: str, token: str
) -> dict[str, Any] | ServiceError:
    is_human = await recaptcha.verify_recaptcha(token)

    if not is_human:
        return ServiceError.RECAPTCHA_VERIFICATION_FAILED

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

    hashed_password = security.hash_password(password)
    account = await accounts.create(
        account_id=uuid4(),
        email=email_address,
        password=hashed_password,
        username=username,
        role=role,
    )

    if account is None:
        return ServiceError.ACCOUNTS_SIGNUP_FAILED

    return account


async def fetch_one(
    id: UUID,
) -> dict[str, Any] | ServiceError:
    account = await accounts.fetch_one(id)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_by_email(
    email: str,
) -> dict[str, Any] | None | ServiceError:
    try:
        account = await accounts.fetch_by_email(email)
        return None if account is None else account
    except Exception:
        return ServiceError.DATABASE_QUERY_FAILED


async def fetch_by_username(
    username: str,
) -> dict[str, Any] | ServiceError:
    account = await accounts.fetch_by_username(username)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_many(
    page: int,
    page_size: int,
) -> list[dict[str, Any]] | None | ServiceError:
    try:
        user_accounts = await accounts.fetch_many(page, page_size)
        return (
            ServiceError.ACCOUNTS_NOT_FOUND if user_accounts is None else user_accounts
        )
    except Exception:
        return ServiceError.DATABASE_QUERY_FAILED


async def fetch_total_count() -> int | ServiceError:
    try:
        total_count = await accounts.fetch_total_count()
    except Exception as e:
        print(e)
        return ServiceError.DATABASE_QUERY_FAILED

    return total_count


async def update_by_id(
    id: UUID,
    username: str | None = None,
    email: str | None = None,
    password: str | None = None,
    role: str | None = None,
) -> dict[str, Any] | ServiceError:
    if username is not None:
        user_exists = await accounts.fetch_by_username(username)
        if user_exists is not None:
            return ServiceError.ACCOUNTS_USERNAME_EXISTS

    if email is not None:
        email_exists = await accounts.fetch_by_email(email)
        if email_exists is not None:
            return ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS

    user_account = await accounts.update_by_id(id, username, email, password, role)

    if user_account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return user_account


async def delete_by_id(
    id: UUID,
) -> dict[str, Any] | ServiceError:
    account = await accounts.delete_by_id(id)

    if account is None:
        return ServiceError.ACCOUNTS_DELETION_FAILED

    return account
