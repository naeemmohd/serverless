import boto3
import os
import json
import decimal

# PLease replace with an actual Step function ARN as this ARN is a test URL
ARN_OF_STATEMACHINE = 'arn:aws:states:us-east-1:123456789012:stateMachine:processPaymentMachine'

sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print('Processing the event:')
    print(event)
    data = json.loads(event['body'])
    data['WaitSeconds'] = int(data['WaitSeconds'])
    
    # Validation Check, if any of the data is missing it will holld a false value in the tuple
    validationCheck = []
    validationCheck.append('WaitSeconds' in data)
    validationCheck.append(type(data['WaitSeconds']) == int)
    validationCheck.append('InvoiceID' in data)
    validationCheck.append('BillersName' in data)
    validationCheck.append('BillingAmount' in data)
    validationCheck.append('CardNumber' in data)
    validationCheck.append('ExpiryDate' in data)

    if data.get('Choices') == "both":
        validationCheck.append('EmailId' in data)
        validationCheck.append('PhnNumber' in data)
    elif data.get('Choices') == "email":
        validationCheck.append('EmailId' in data)
    elif data.get('Choices') == "text":
        validationCheck.append('PhnNumber' in data)

    # Check for any FALSE value in  validationCheck
    if False in validationCheck:
        response = {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps(
                {
                    "Status": "Success", 
                    "Reason": "Sorry, please verify the data you posted and try again!!!"
                },
                cls=DecimalEncoder
            )
        }
    else: 
        sfn.start_execution(
            stateMachineArn=ARN_OF_STATEMACHINE,
            input=json.dumps(data, cls=DecimalEncoder)
        )
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps(
                {"Status": "Success"},
                cls=DecimalEncoder
            )
        }
    return response

# This is a workaround for: http://bugs.python.org/issue16535
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

