from src.utilities.mapMcc import map_mcc_to_category
from src.models.TransactionModel import TransactionModel
import boto3
from bson import json_util
import json

# Possível solução para L4. Questão aberta. Esta é uma 
# ideia possível para a questão L4, porém ela não foi testada. 

# AWS SQS setup
sqs = boto3.client('sqs', region_name='us-east-1')
account_queues = {}  

class SimultaneousTransactionsService:

    async def get_or_create_queue(account):
        if account in account_queues:
            return account_queues[account]
        
        response = sqs.create_queue(QueueName=f"{account}_transactions")
        account_queues[account] = response['QueueUrl']
        return account_queues[account]

    async def sqs_send_message(queue_url: str, payload: TransactionModel):
        doc = json_util.dumps(payload)
        body = json.loads(doc)

        # Enviar a transação para a fila SQS
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(body)
        )
        return response

