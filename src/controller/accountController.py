from fastapi import APIRouter, HTTPException
from src.models.AccountModel import AccountModel
from src.database.schema import SchemaOutput
from src.service.accountService import AccountService

account_router = APIRouter(prefix='/account')

@account_router.get('/accounts', status_code=200)
async def list_accounts():
    try: 
        response = await AccountService.list_accounts()
        return SchemaOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@account_router.post('/create', status_code=200)   
async def create_account(accountModel: AccountModel):
    try:
        await AccountService.create_account(accountModel)

    except HTTPException as error:
        raise HTTPException(400, detail=str(error))


