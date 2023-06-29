from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from fastapi import APIRouter
from server.services import accounts
from server.utils.errors import ServiceError
from server.api.rest import responses
from server.api.rest.v1.accounts import Account

router = APIRouter(tags=["Search"])


class EmailRequest(BaseModel):
    email: str


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
