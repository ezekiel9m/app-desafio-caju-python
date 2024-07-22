from src.database.connDynamoDB import dynamodb
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

try:
    # Crie uma tabela accounts
    table_accounts = 'accounts'
    table = dynamodb.create_table(
        TableName=table_accounts,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Aguarde a criação da tabela accounts
    table.meta.client.get_waiter('table_exists').wait(TableName=table_accounts)
    print(f'Table {table_accounts} created successfully.')

    # Insira um item de accounts
    table.put_item(
        Item={
            "accountId": "123",
            "balances": {
                "FOOD": 500.0,
                "MEAL": 700.0,
                "CASH": 1000.0
            }
        }
    )
    print('Item inserted successfully.')

    # Crie uma tabela accounts
    table_transactions = 'transactions'
    table = dynamodb.create_table(
        TableName=table_transactions,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Aguarde a criação da tabela
    table.meta.client.get_waiter('table_exists').wait(TableName=table_transactions)
    print(f'Table {table_transactions} created successfully.')
   
    # Insira um item de transactions
    table.put_item(
        Item={
            "account": "123",
            "totalAmount": 100.00,
            "mcc": "5811",
            "merchant": "PADARIA DO ZE  SAO PAULO BR"
        }
    )
    print('Item inserted successfully.')

except NoCredentialsError:
    print("Error: AWS credentials not provided.")
except PartialCredentialsError:
    print("Error: Incomplete AWS credentials provided.")
except Exception as e:
    print(f"An error occurred: {e}")
