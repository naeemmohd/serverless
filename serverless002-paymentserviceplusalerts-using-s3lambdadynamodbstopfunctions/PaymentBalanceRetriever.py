import boto3
import csv 
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
	
def handler(event, context):
    # Get the object from the event then download it to Lambda tmp space
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    if '.csv' not in key:
        return 'Not a csv that needs processing'
    s3.download_file(bucket, key, '/tmp/' + key)
    # Use DynamoDB atomic counters to tally visits in csv
    with open('/tmp/' + key, 'r') as infile:
        first_line = infile.readline()
        for row in infile:
            ddb_InvoiceId = row.strip().split(',')[0]
            ddb_CustomerName = row.strip().split(',')[1]
            ddb_Balance = row.strip().split(',')[2]
            ddb_Processed = row.strip().split(',')[3]
            response = dynamodb.update_item(
                    TableName='PaymentBalance', 
                    Key={
                        'InvoiceID': {'N': ddb_InvoiceId}
                    },
                    UpdateExpression='set Balance=:balance, IsProcessed=:processed, CustomerName=:customerName',
                    ExpressionAttributeValues={
                        ':balance': {'N': ddb_Balance},
                        ':processed': {'N': ddb_Processed},
                        ':customerName': {'S': str(ddb_CustomerName)}
                    },
                    ReturnValues="UPDATED_NEW"
            )
            print(response)