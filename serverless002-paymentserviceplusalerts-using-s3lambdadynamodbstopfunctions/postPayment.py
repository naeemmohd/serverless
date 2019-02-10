import boto3
import csv 
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # assuming the payment was process by a third party after passing payment info securily and encrypted.
    # another lambda function can handle the real payment processing via a third party
    invoiceId = event['InvoiceID']
    billerName = event['BillersName']
    # manually seeting balance as 0 and isprocessed as 1 simulate as if a payment was done.
    balance = 0
    isprocessed = 1
    response = dynamodb.update_item(
        TableName='PaymentBalance', 
        Key={
            'InvoiceID': {'N': invoiceId}
        },
        UpdateExpression='set Balance=:balance, IsProcessed=:processed, CustomerName=:customerName',
        ExpressionAttributeValues={
            ':balance': {'N': str(balance)},
            ':processed': {'N': str(isprocessed)},
            ':customerName': {'S': str(billerName)}
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    return event;

