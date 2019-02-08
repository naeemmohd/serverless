import boto3
import csv 
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def deleteTable(table_name):
    print('deleteting table')
    return dynamodb.delete_table(TableName=table_name)
	
def createTable(table_name):
    waiter = dynamodb.get_waiter('table_not_exists')
    waiter.wait(TableName=table_name)
    print('creating table')
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'InvoiceID',
                'KeyType': 'HASH'
            },
			{
                'AttributeName': 'CustomerName',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions= [
			{
                'AttributeName': 'InvoiceID',
                'AttributeType': 'N'
            }
            {
                'AttributeName': 'CustomerName',
                'AttributeType': 'S'
            },
                        {
                'AttributeName': 'Balance',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 3,
            'WriteCapacityUnits': 3
        },
        StreamSpecification={
            'StreamEnabled': False
        }
    )
	
def emptyTable(table_name):
    deleteTable(table_name)
	createTable(table_name)
	
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
    emptyTable('PaymentBalance')
    with open('/tmp/' + key, 'r') as infile:
        first_line = infile.readline()
        for row in infile:
            ddb_InvoiceId = row.strip().split(',')[0]
            ddb_CustomerName = row.strip().split(',')[1]
            ddb_Balance = row.strip().split(',')[2]
            response = dynamodb.put_item(
                    TableName='PaymentBalance', 
					Item: {
					  InvoiceID: { 'N', ddb_InvoiceId },
					  CustomerName: { 'S', ddb_CustomerName },
					  Balance: { 'N', ddb_Balance }
					},
                    ReturnValues="ALL_NEW"
            )
            print(response)
