import names
import random
import os

dirName = 'logs';
if not os.path.exists(dirName):
    os.mkdir(dirName)
    
# categories csv file
filePath = dirName + '/categories.csv';
with open(filePath, 'w+') as outfile:
    outfile.write('CategoryID,CategoryName,IsActive\n')
    outfile.write('1,\'Skin care\',1\n')
    outfile.write('2,\'Make up\',1\n')
    outfile.write('3,\'Fragnance\',1\n')
    outfile.close()
    print('Please check the file at path:' + os.path.abspath(filePath));
    
# sub categories csv file
filePath = dirName + '/subcategories.csv';
with open(filePath, 'w+') as outfile:
    outfile.write('SubCategoryID,SubCategoryName,CategoryID,IsActive\n')
    outfile.write('1,\'Exfoliator\',1,1\n')
    outfile.write('2,\'Serum\',1,1\n')
    outfile.write('3,\'Lipstick\',2,1\n')
    outfile.write('4,\'Eye Liner\',2,1\n')
    outfile.write('5,\'Mens\',3,1\n')
    outfile.write('6,\'Womans\',3,1\n')
    outfile.close()
    print('Please check the file at path:' + os.path.abspath(filePath));  

# promotions csv file
filePath = dirName + '/promotions.csv';
with open(filePath, 'w+') as outfile:
    outfile.write('PromotionID,PromotionName,PromotionDiscount,IsActive\n')
    outfile.write('1,\'New Cosultant Promotions\',20,1\n')
    outfile.write('2,\'Senior Cosultant Promotions\',30,1\n')
    outfile.write('3,\'Director Level Promotions\',50,1\n')
    outfile.close()
    print('Please check the file at path:' + os.path.abspath(filePath));

# products csv file
filePath = dirName + '/products.csv';
with open(filePath, 'w+') as outfile:
    outfile.write('ProductID,ProductName, ProductDescription, Price, CategoryID, SubCategoryID,PromotionID, IsActive\n')
    outfile.write('1,\'Tan Lipstick\', \'This product is a tan shade lipstick\', 45, 1, 1, 1, 1\n')
    outfile.write('2,\'Lemon Scrub\', \'This product helps exfoliate your skin with lemon flavor\', 55, 2, 3, 2, 1\n')
    outfile.write('3,\'Glory Miracle Special\', \'This is a directors special all in one best product\', 65, 3, 6, 3, 1\n')
    outfile.close()
    print('Please check the file at path:' + os.path.abspath(filePath));