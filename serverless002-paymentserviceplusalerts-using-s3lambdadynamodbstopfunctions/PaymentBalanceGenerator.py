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


