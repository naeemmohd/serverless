# Prerequisites: Please install the following befor genarating the file.
# install pip and dependencies
# sudo apt-get install python-pip python-dev build-essential
# install names 
# pip install names
import names
import random
monthNumbers = range(1,26)
for monthNumber in monthNumbers:
    with open('logs/salarydata-' + str(monthNumber) + '.csv', 'w+') as outfile:
        numRows = range(1,101)
        outfile.write('EmpID,EmpName,EmpSalary\n')
        strRow = ''
        for numRow in numRows:
            if numRow % 2 == 0:
                strRow = str(monthNumber) + str(numRow) + ',' + names.get_full_name(gender='male') + ',' + str(random.randint(5555, 7777))
            else:
                strRow = str(monthNumber) + str(numRow) + ',' + names.get_full_name(gender='female') + ',' + str(random.randint(5555, 7777))
            outfile.write(strRow + '\n')
        outfile.close()
            


