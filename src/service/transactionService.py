from fastapi import HTTPException
from src.utilities.mapMcc import map_mcc_to_category
from src.models.TransactionModel import TransactionModel
from src.database.connMongoDB import accounts_collection, transactions_collection
from uuid import UUID, uuid4

class TransactionService:
    async def list_transactions() -> list:
       return list(transactions_collection.find())

    async def process_transaction(payload: TransactionModel):
        account_id = payload.account
        mcc = payload.mcc
        total_amount = payload.totalAmount
        merchant = payload.merchant
        
        # Substituição de MCC baseado no nome do comerciante (L3)
        # Substituição de MCC baseado no nome do comerciante (L3)
        merchant_item = {
            "UBER TRIP                   SAO PAULO BR": "4111",
            "UBER EATS                   SAO PAULO BR": "5812",
            "PAG*JoseDaSilva          RIO DE JANEI BR": "5311",
            "PICPAY*BILHETEUNICO           GOIANIA BR": "4111"
        }

        if merchant in merchant_item:
            mcc = merchant_item[merchant]

        category= map_mcc_to_category(mcc)
        print(category)

        account = accounts_collection.find_one({"accountId": account_id})

        if not account:
            raise HTTPException(status_code=400, detail="Account not found")

        balances = account["balances"]
        
        # Verifica saldo suficiente na categoria principal (L1)
        if balances[category] >= total_amount:
            balances[category] -= total_amount
        else:
            # Verifica saldo em CASH como fallback (L2)
            if category != "CASH" and balances["CASH"] >= total_amount:
                balances["CASH"] -= total_amount
            else:
                return {"code": "51"}  # Transação rejeitada por saldo insuficiente
        
        # Atualiza os saldos no MongoDB
        accounts_collection.update_one({"accountId": account_id}, {"$set": {"balances": balances}})
        
        # Registra a transação no MongoDB
        transaction_record = {
            "id": str(uuid4()),
            "accountId": account_id,
            "amount": total_amount,
            "merchant": merchant,
            "mcc": mcc
        }
        transactions_collection.insert_one(transaction_record)
        return {"code": "00"}  # Transação aprovada
        
    




