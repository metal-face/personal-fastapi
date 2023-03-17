from datetime import datetime
from uuid import UUID

from server.utils import logger
from server.services import sessions
from server.utils.errors import ServiceError
from server.api.rest import responses
from server.models.dto.sessions import LoginForm
from fastapi import status
from fastapi import Header


def get_status_code(error: ServiceError) -> int:
    if error is ServiceError.CREDENTIALS_INCORRECT:
        return status.HTTP_401_UNAUTHORIZED
    elif error is ServiceError.SESSIONS_NOT_FOUND:
        return status.HTTP_404_NOT_FOUND
    else:
        logger.error("Unhandled service error: ", error=error)
        return status.HTTP_500_INTERNAL_SERVER_ERROR


@router.post("/v1/sessions", response_model=responses.success)
async def login(
    args: LoginForm,
    user_agent: str = Header(...),
):
    data = await sessions.login(
        username=args.username, password=args.password, user_agent=user_agent
    )

    if isinstance(data, ServiceError):
        return responses.failure(
            content=data,
            status_code=get_status_code(data),
        )
