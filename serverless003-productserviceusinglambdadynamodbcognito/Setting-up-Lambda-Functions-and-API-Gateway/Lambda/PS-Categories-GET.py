import boto3
import decimal
import json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('PS-Categories')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def handler(event, context):
    # PS-Categorie - Partion Key: CategoryID, Attributes: CategoryName, IsActive
    filterExpression = Attr('IsActive').between(0, 1)
    projectionExpression = "CategoryID, CategoryName, IsActive"
    # Expression Attribute Names for Projection Expression only.
    # expressionAttributeNames = { "#yr": "year", }
    
    response = table.scan(
        FilterExpression=filterExpression,
        ProjectionExpression=projectionExpression #,
        #ExpressionAttributeNames=ean
    )

    for i in response['Items']:
        print(json.dumps(i, cls=DecimalEncoder))


