import boto3
import csv 
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def handler(event, context):
# Get the object from the event then download it to Lambda tmp space
bucket = event['Records'][0]['s3']['bucket']['name']
print(bucket)
key = event['Records'][0]['s3']['object']['key']
print(key)
if '.csv' not in key:
    return 'Not a csv file, please upload a CSV File.'
s3.download_file(bucket, key, '/tmp/' + key)
# Use DynamoDB atomic counters to sget data from csv and save to DynamoDB
with open('/tmp/' + key, 'r') as infile:
    first_line = infile.readline()
    if 'categories' in key and 'subcategories' not in key:
        for row in infile:
            print(row)
            dbCategoryID = row.strip().split(',')[0]
            dbCategoryName = row.strip().split(',')[1]
            dbIsActive = row.strip().split(',')[2]
            response = dynamodb.update_item(
                    TableName='PS-Categories', 
                    Key={
                        'CategoryID': {'N': dbCategoryID}
                    },
                    UpdateExpression='set CategoryName=:categoryName, IsActive=:isActive',
                    ExpressionAttributeValues={
                        ':categoryName': {'S': dbCategoryName},
                        ':isActive': {'N': dbIsActive}
                    },
                    ReturnValues="UPDATED_NEW"
            )
            print(response)
    elif 'subcategories' in key
        for row in infile:
            print(row)
            dbSubCategoryID= row.strip().split(',')[0]
            dbSubCategoryName = row.strip().split(',')[1]
            dbCategoryID = row.strip().split(',')[2]
            dbIsActive = row.strip().split(',')[3]
            response = dynamodb.update_item(
                    TableName='PS-SubCategories', 
                    Key={
                        'SubCategoryID': {'N': dbSubCategoryID}
                    },
                    UpdateExpression='set SubCategoryName=:subCategoryName, CategoryID=:categoryID, IsActive=:isActive',
                    ExpressionAttributeValues={
                        ':subCategoryName': {'S': dbSubCategoryName},
                        ':categoryID': {'N': dbCategoryID},
                        ':isActive': {'N': dbIsActive}
                    },
                    ReturnValues="UPDATED_NEW"
            )
            print(response)
    elif 'promotions' in key
        for row in infile:
            print(row)
            dbPromotionID= row.strip().split(',')[0]
            dbPromotionName = row.strip().split(',')[1]
            dbPromotionDiscount = row.strip().split(',')[2]
            dbIsActive = row.strip().split(',')[3]
            response = dynamodb.update_item(
                    TableName='PS-Promotions', 
                    Key={
                        'PromotionID': {'N': dbPromotionID}
                    },
                    UpdateExpression='set PromotionName=:promotionName, PromotionDiscount=:promotionDiscount, IsActive=:isActive',
                    ExpressionAttributeValues={
                        ':promotionName': {'S': dbPromotionName},
                        ':promotionDiscount': {'N': dbPromotionDiscount},
                        ':isActive': {'N': dbIsActive}
                    },
                    ReturnValues="UPDATED_NEW"
            )
            print(response)
    elif 'products' in key
        for row in infile:
            print(row)
            dbProductID= row.strip().split(',')[0]
            dbProductName = row.strip().split(',')[1]
            dbProductDescription = row.strip().split(',')[2]
            dbPrice = row.strip().split(',')[3]
            dbCategoryID = row.strip().split(',')[4]
            dbSubCategoryID = row.strip().split(',')[5]
            dbPromotionID = row.strip().split(',')[6]
            dbIsActive = row.strip().split(',')[7]
            response = dynamodb.update_item(
                    TableName='PS-Products', 
                    Key={
                        'ProductID': {'N': dbProductID}
                    },
                    UpdateExpression='set ProductName=:productName, ProductDescription=:productDescription, Price=:price, CategoryID=:categoryID, SubCategoryID=:subCategoryID, PromotionID=:promotionID, IsActive=:isActive',
                    ExpressionAttributeValues={
                        ':productName': {'S': dbProductName},
                        ':productDescription': {'S': dbProductDescription},
                        ':price': {'N': dbPrice},
                        ':categoryID': {'N': dbCategoryID},
                        ':subCategoryID': {'N': dbSubCategoryID},
                        ':promotionID': {'N': dbPromotionID},
                        ':isActive': {'N': dbIsActive}
                    },
                    ReturnValues="UPDATED_NEW"
            )
            print(response)