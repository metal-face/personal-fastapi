from fastapi import APIRouter
from server.models.dto.AccountDTO import AccountDTO
from server.repositories import accounts

router = APIRouter()

@router.post("/accounts")
async def create_account(args: AccountDTO):
    accounts.create_account()