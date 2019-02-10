# Payment processor with work flow state machine using Data using AWS S3, Lambda Functions, Step Functions and DynamoDB.
### This article shows how to use these AWS services - S3, Lambda Functions, Step Functions and DynamaDB to process a payment.
### Objective:
- For the Billling and Payment process, a file is placed/updated in S3 everyday for customers whose Bill is due/pending and
- Next, this Bills Due file is processed by a Lambda Function to update the information in a DynamoDB table and
- Next, on the Billings Website, a customer retrives his bill by entering his Invoice ID and makes a payment and
- Next, the payment is processed and Balance is updated to zero and 
- Finally, a text or email alert is sent to customer confirming his payment

### Lets tabulate the steps as below:
Steps | Actions
------------ | -------------
Prerequisite | Generate the 'Bills Due' file for specific day 
S3 | Create a S3 bucket and upload the 'Bills Due' file
DynamoDB | Create a table to store 'Bills Due'
Lambda Functions | Create functions to update DynamoDB database with 'Bills Due' info, email and text alert, process payment etc
Step Function | Create a Step function to create a work flow which will process the payment and send email/text alert 


#### Prerequisite - Generate the 'Bills Due' file for specific day  
 - I am using an arbitrary logic to generate the file.
 - Once generated, the file will look like below
   ![Payment Balance CSV file](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/bucketsnap01.png)
 - Here is the code for the file(PaymentBalanceGenerator.py):
  ```
  # Prerequisites: Please install the following before genarating the file.
  # install pip and dependencies
  # sudo apt-get install python-pip python-dev build-essential
  # install names 
  # pip install names
  import names
  import random
  import os

  dirName = 'logs';
  if not os.path.exists(dirName):
      os.mkdir(dirName)

  filePath = dirName + '/paymentbalance.csv';
  with open(filePath, 'w+') as outfile:
      numRows = range(1,1001)
      outfile.write('InvoiceID,CustomerName,Balance,IsProcessed\n')
      strRow = ''
      for numRow in numRows:
          strRow = str(numRow) + ',' + names.get_full_name(gender='female') + ',' + str(random.randint(500, 900)) + ',0'
          outfile.write(strRow + '\n')
      outfile.close()

  print('Please check the file at path:' + os.path.abspath(filePath));            
  ```
- Now save and execute the above python file(DataFileGnerator.py):
  ```
  python DataFileGnerator.py
  ```
#### S3	Create a S3 bucket to upload
- Create a bucket name - any universally unique name is okay. 
  - Lets put the name as - S3BucketProcessSalaryData2019
- Please see the snapshot below
  ![Creating Bucket Snap 01](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/bucketsnap01.png)
  ![Creating Bucket Snap 02](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/bucketsnap02.png)
#### Lambda | Create a Lambda function with a trigger which gets invokes as a file is uplaoded to S3 
- Create a Lambda function named - process_slary_data. 
  - Add a trigger to invoke on any item add to the above bucket
  - Add the function code as below:
    ```
    # **import boto3, csv and json packages**
    import boto3
    import csv 
    import json

    # **generate variables for S3 and DynamoDB clients**
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')

    # **The main lambda handler function**
    def handler(event, context):
        # **get the bucket name and salary data file name as key**
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        # **Dont process if the files does not have a .csv extn**
        if '.csv' not in key:
            return 'Please upload .csv files only.'
        if '.psv' in key:
            return 'This .psv file is already proccessed'
        # **download the .csv file to /tmp folder**
        s3.download_file(bucket, key, '/tmp/' + key)
        psvName = 'processed_' + key[0:-4] + '.psv'
        # Open the .csv file to process it, and upload the processed .psv file
        with open('/tmp/' + key, 'r') as infile, \
             open('/tmp/' + psvName, 'w') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, reader.fieldnames, delimiter='|')
            writer.writeheader()
            writer.writerows(reader)
        s3.upload_file('/tmp/' + psvName, bucket, psvName)
        # Use the DynamoDB atomic counters to add/update data in the DynamoDB
        with open('/tmp/' + key, 'r') as infile:
            first_line = infile.readline()
            for row in infile:
                ddb_empId = row.strip().split(',')[0]
                ddb_empName = row.strip().split(',')[1]
                ddb_empSalary = row.strip().split(',')[2]
                response = dynamodb.update_item(
                        TableName='EmployeeSalary', 
                        Key={
                            'EmpID': {'N': ddb_empId},
                            'EmpName': {'S': ddb_empName},
                        },
                        UpdateExpression='ADD EmpSalary :empSalary',
                        ExpressionAttributeValues={
                            ':empSalary': {'N': ddb_empSalary}
                        },
                        ReturnValues="UPDATED_NEW"
                )
                print(response)
    ```
- Please see the snapshot below
  ![Creating Lambda Function Snap 01](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/lambdasnap01.png)
  ![Creating Lambda Function Snap 02](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/lambdasnap02.png)
  ![Creating Lambda Function Snap 03](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/lambdasnap03.png)
#### DynamoDB | Once the file is getting processed keep writing and updating the data in a table
- Create a DynamoDB table 'EmployeeSalary' with Primary Key as 'EmpID' and Sort Key as 'EmpName'.
- Please see the snapshot below.
  ![Creating Lambda Function Snap 03](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/ddbsnap01.png)
#### Once the above steps are ready
- Drag and drop the generated salary data files in the S3 bucket.
- Check if another .psv files is also generated
- Check the DynamoDB tablea to see if your salary data is sucessfully written.
- Please see the snapshot below.
  ![Creating Lambda Function Snap 03](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/uploadfile.png)
  ![Creating Lambda Function Snap 03](https://github.com/naeemmohd/serverless/blob/master/serverless001-processdata-using-s3lambdadynamodb/images/result.png)
