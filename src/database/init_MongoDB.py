from asyncio import run
from database.connMongoDB import accounts_collection, transactions_collection, client

db = client["cuju_db"]
async def create_collections():
    account = 'accounts'
    transaction = 'transactions'

    if check_and_create_collection(account) == False:
        account_item = {
            "accountId": "123",
            "balances": {
                "FOOD": 500.0,
                "MEAL": 500.0,
                "CASH": 1000.0
            }
        }
        db.create_collection(account)
        accounts_collection.insert_one(account_item)

    if check_and_create_collection(transaction) == False:
        transaction_item = {
            "account": "123",
            "totalAmount": 100.00,
            "mcc": "5811",
            "merchant": "PADARIA DO ZE  SAO PAULO BR"
        }
        db.create_collection(transaction)
        transactions_collection.insert_one(transaction_item)

# Função para verificar se a coleção existe e criar se não existir
def check_and_create_collection(col_name):
    if col_name not in db.list_collection_names():
        print(f'the collection "{col_name}" does not exist')
        return False
    else:
        print(f'the collection "{col_name}" already exist.')  
        return True

if __name__ == '__main__':
    run(create_collections())
