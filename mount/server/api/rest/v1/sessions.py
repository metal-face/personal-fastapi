from datetime import datetime
from uuid import UUID

from server.utils import logger
from server.services import sessions
from server.utils.errors import ServiceError
from server.api.rest.responses import Success, Failure, failure, success
from server.api.rest.authorization import HTTPBearer, HTTPAuthorizationCredentials
from server.models.dto.sessions import LoginForm
from server.models.entities.sessions import Session
from fastapi import Header, status, APIRouter, Depends
from typing import Union

router = APIRouter(tags=["Sessions"])
http_scheme = HTTPBearer(auto_error=False)


def get_status_code(error: ServiceError) -> int:
    if error is ServiceError.CREDENTIALS_INCORRECT:
        return status.HTTP_401_UNAUTHORIZED
    elif error is ServiceError.SESSIONS_NOT_FOUND:
        return status.HTTP_404_NOT_FOUND
    else:
        logger.error("Unhandled service error: ", error=error)
        return status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post("/sessions", response_model=Success[Session])
async def login(
    args: LoginForm,
    user_agent: str = Header(...),
):
    data = await sessions.login(
        username=args.username,
        password=args.password,
        user_agent=user_agent,
    )

    if isinstance(data, ServiceError):
        return failure(
            error=data,
            message="Failed to create session",
            status_code=get_status_code(data),
        )

    resp = Session.from_mapping(data)

    return success(
        resp,
        status_code=status.HTTP_201_CREATED,
        cookies=[
            {
                "key": "session_id",
                "value": data["session_id"],
                "httponly": False,
                "secure": False,
                "samesite": "lax",
                "expires": int((data["expires_at"] - datetime.now()).total_seconds()),
            }
        ],
    )


@router.get("/sessions")
async def fetch_many(
    account_id: UUID | None = None,
    user_agent: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> Union[Success[list[Session]], Failure]:
    data = await sessions.fetch_many(
        account_id=account_id,
        user_agent=user_agent,
        page=page,
        page_size=page_size,
    )

    if isinstance(data, ServiceError):
        return failure(
            error=data,
            message="Failed to find any sessions",
            status_code=get_status_code(data),
        )

    resp = [Session.from_mapping(rec) for rec in data]
    return success(resp)


@router.get("/sessions/{session_id}")
async def fetch_session_by_id(session_id: UUID) -> Union[Success[Session], Failure]:
    data = await sessions.fetch_one(session_id=session_id)

    if isinstance(data, ServiceError):
        return failure(
            error=data,
            message="Failed to find session!",
            status_code=get_status_code(data),
        )

    resp = Session.from_mapping(data)
    return success(resp)


@router.delete("/sessions")
async def logout(
    http_credentials: HTTPAuthorizationCredentials | None = Depends(http_scheme),
) -> Union[Success[Session], Failure]:
    if http_credentials is None:
        return failure(
            error=ServiceError.SESSIONS_NOT_FOUND,
            message="Failed to log out of session!",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    data = await sessions.logout(session_id=http_credentials.credentials)

    if isinstance(data, ServiceError):
        return failure(
            error=data,
            message="Failed to log out of session!",
            status_code=get_status_code(data),
        )

    resp = Session.from_mapping(data)
    return success(resp, status_code=status.HTTP_200_OK)
