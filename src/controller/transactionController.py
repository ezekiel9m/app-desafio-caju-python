from fastapi import APIRouter, HTTPException
from src.models.TransactionModel import TransactionModel
from src.database.schema import SchemaOutput
from src.service.transactionService import TransactionService
from src.service.simultaneousTransactionsService import SimultaneousTransactionsService
import uvicorn

app_router = APIRouter(prefix='/transaction')
    
@app_router.get('/transactions', status_code=200)
async def list_transactions():
    try: 
        response = await TransactionService.list_transactions()
        return SchemaOutput(response)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@app_router.post('/authorize', status_code=200)   
async def transaction(payload: TransactionModel):
    try:
        response = await TransactionService.process_transaction(payload)
        return response 
    except HTTPException as error:
        raise HTTPException(400, detail=str(error))
    except Exception as e:
        return {"code": "07"}  # Qualquer outro problema



#Possível solução para L4. Questão aberta
@app_router.post("/simultaneous/transactions")
async def simultaneous_transactions(payload: TransactionModel):

    try:
        queue_url = await SimultaneousTransactionsService.get_or_create_queue(payload.Account_id)
        await SimultaneousTransactionsService.sqs_send_message(queue_url, payload)

    except HTTPException as error:
        raise HTTPException(400, detail=str(error))
    except Exception as e:
        return {"code": "07"}  # Qualquer outro problema
        
    




