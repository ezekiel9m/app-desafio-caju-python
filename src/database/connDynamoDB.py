import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure suas credenciais 
localstack_url = ''
aws_access_key_id = ''
aws_secret_access_key = ''
region_name = 'us-west-1'  

try:
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Conecta ao recurso DynamoDB no LocalStack
    dynamodb = session.resource(
        'dynamodb',
        endpoint_url=localstack_url  # Endpoint do LocalStack
    )

    print("Successful connection to DynamoDB in LocalStack!")

    response = dynamodb.list_tables()
    #tables = response.get('TableNames')

    if len(response) > 0:
        accounts_tb = dynamodb.Table('accounts')
        transaction_tb = dynamodb.Table('transaction')
    else:
        print("No tables found.")

except NoCredentialsError:
    print("Error: Credentials not provided.")
except PartialCredentialsError:
    print("Error: Incomplete credentials provided.")
except Exception as e:
    print(f"Error connecting to DynamoDB in LocalStack: {e}")




