
from pymongo import MongoClient, errors
database_url_atlas =''

try:
    #database_url_atlas = getenv('database_url_atlas')
    client = MongoClient(database_url_atlas, serverSelectionTimeoutMS=5000) 

    db = client['cuju_db']
    accounts_collection = db.accounts
    transactions_collection= db.transactions

except errors.ServerSelectionTimeoutError as err:
    # Trate o erro de timeout
    print("Error: Timeout was reached.")
    print(err)

except errors.ConnectionFailure as err:
    # Trate o erro de conexão
    print("Error: Connection failed.")
    print(err)



