"""
Importing and combining all CSVs, can be reused to import CSV files containing 
particular dates in strings
"""

import csv
import os
import glob
import pandas as pd
#set working directory
os.chdir(r"/Users/steve/OneDrive/ANU/COMP1730_SEM2_2021/covid-data/covid-data")
# os.chdir(r"C:\Users\steve\OneDrive\ANU\COMP1730_SEM2_2021\covid-data\covid-data")

#find all csv files in the folder
#use glob pattern matching -> extension = 'csv'
#save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#print(all_filenames)


table_list = []
selected_csv_table = []
for filename in os.listdir(r"/Users/steve/OneDrive/ANU/COMP1730_SEM2_2021/covid-data/covid-data"):
# for filename in os.listdir(r"C:\Users\steve\OneDrive\ANU\COMP1730_SEM2_2021\covid-data\covid-data"):
    if filename.endswith('.csv'):
        table_list.append(pd.read_csv(filename,sep="|"))
        selected_csv_table.append(filename.split(".")[0])


#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

"""
------------------------------------------------------------------------------
Importing one single csv
import csv

with open("09-14-2021.csv") as csvfile:
    reader = csv.reader(csvfile)
    count = 0

    for row in reader:
            count = count + 1
            print (row)
            if count > 10:
                break

------------------------------------------------------------------------------
"""

with open("combined_csv.csv") as csvfile:
    reader = csv.reader(csvfile)
    count = 0

    for row in reader:
            count = count + 1
            print (row)
            if count > 10:
                break
            
"""
------------------------------------------------------------------------------
"""
            
            