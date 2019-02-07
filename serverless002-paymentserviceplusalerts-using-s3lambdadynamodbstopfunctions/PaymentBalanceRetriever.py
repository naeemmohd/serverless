import boto3
import csv 
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def handler(event, context):
    # Get the object from the event then download it to Lambda tmp space
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # IMPORTANT:
    if '.csv' not in key:
        return 'Not a csv that needs processing'
    if '.psv' in key:
        return 'An already processed logfile'
    s3.download_file(bucket, key, '/tmp/' + key)
    # Use DynamoDB atomic counters to tally visits in csv
    with open('/tmp/' + key, 'r') as infile:
        first_line = infile.readline()
        for row in infile:
            ddb_InvoiceId = row.strip().split(',')[0]
            ddb_CustomerName = row.strip().split(',')[1]
            ddb_Balance = row.strip().split(',')[2]
            response = dynamodb.update_item(
                    TableName='EmployeeSalary', 
                    Key={
                        'InvoiceID': {'N': ddb_InvoiceId},
                        'CustomerName': {'S': ddb_CustomerName},
                    },
                    UpdateExpression='ADD Balance :balance',
                    ExpressionAttributeValues={
                        ':balance': {'N': ddb_Balance}
                    },
                    ReturnValues="UPDATED_NEW"
            )
            print(response)
