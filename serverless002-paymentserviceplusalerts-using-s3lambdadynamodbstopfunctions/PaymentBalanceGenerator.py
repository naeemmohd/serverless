# Prerequisites: Please install the following before genarating the file.
# install pip and dependencies
# sudo apt-get install python-pip python-dev build-essential
# install names 
# pip install names
import names
import random
with open('logs/paymentbalance.csv', 'w+') as outfile:
    numRows = range(1,1001)
    outfile.write('InvoiceID,CustomerName,Balance\n')
    strRow = ''
    for numRow in numRows:
        strRow = str(numRow) + ',' + names.get_full_name(gender='female') + ',' + str(random.randint(500, 900))
        outfile.write(strRow + '\n')
    outfile.close()
            


