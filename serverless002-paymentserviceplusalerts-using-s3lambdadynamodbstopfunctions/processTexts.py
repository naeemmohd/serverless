import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    sns_msg = 'A payment of amount:' + event['BillingAmount'] + ' has been processed for Invoice Id:' + event['InvoiceID'] + '.'
    sns.publish(PhoneNumber=event['PhnNumber'], Message=sns_msg)
    return 'Success!'