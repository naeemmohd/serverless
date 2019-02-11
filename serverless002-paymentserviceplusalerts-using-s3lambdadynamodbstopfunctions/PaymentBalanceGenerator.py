# Prerequisites: Please install the following before genarating the file.
# install pip and dependencies
# for Python 2.x - sudo apt-get install python-pip python-dev build-essential python-setuptools
# for Python 3.x - sudo apt-get install python3-pip python3-dev build-essential python3-setuptools
# install names 
# for Python 2.x - pip install names
# for Python 3.x - pip3 install names

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


