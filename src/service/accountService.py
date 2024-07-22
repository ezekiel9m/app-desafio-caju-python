from src.models.AccountModel import AccountModel
from src.database.connMongoDB import accounts_collection
import random 

class AccountService:
    async def list_accounts() -> list:
       return list(accounts_collection.find())
    
    async def create_account(accountModel: AccountModel):
        account_id = random.randint(1000, 3)

        new_account = {
            "accountId": str(account_id),
            "balances": {
                "FOOD": accountModel.Food,
                "MEAL": accountModel.Meal,
                "CASH": accountModel.Cash
            }
        }
        accounts_collection.insert_one(new_account)
    

    
        
    




