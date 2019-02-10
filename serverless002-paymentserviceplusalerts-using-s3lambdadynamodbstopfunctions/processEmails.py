import boto3

VERIFIED_EMAIL = 'tpml9090@gmail.com'

ses = boto3.client('ses')

def lambda_handler(event, context):
    
    email_subject = 'A payment of amount:' + event['BillingAmount'] + ' has been processed for Invoice Id:' + event['InvoiceID'] + '.'
    email_body = ' Mr./Ms. ' + event['BillersName'] + '\n Thank you, \n A payment of amount:' + event['BillingAmount'] + ' has been processed for Invoice Id:' + event['InvoiceID'] + '.'
    
    ses.send_email(
        Source=VERIFIED_EMAIL,
        Destination={
            'ToAddresses': [event['EmailId']]
        },
        Message={
            'Subject': {'Data': email_subject},
		    'Body': {'Text' : {'Data': email_body }}
        }
    )
    return 'Success!'