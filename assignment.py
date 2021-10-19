"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/


The assignment is due 25/10/2021 at 9:00 am, Canberra time

Collaborators: <list the UIDs of ALL members of your project group here>
"""

import pandas as pd
import os

def analyse(path_to_files):
    # Q1a
    covid_files_list  = os.listdir(path_to_files)[1:]
    
    # find most recent file by first finding the latest date, then day    
    recent_file = find_most_recent_file(covid_files_list)
   
    covid_data = pd.read_csv(path_to_files+"/" + recent_file)
    
    latest_last_update = last_update(covid_data)
    
    # Q1b
    ww_cases = sum(covid_data["Confirmed"])
    ww_deaths = sum(covid_data["Deaths"])
    
    # Q2a, Q2b
    temp_file_list = covid_files_list.copy()
    temp_file_list.remove(recent_file)
    day_before_file = find_most_recent_file(temp_file_list)    
    day_before_data = pd.read_csv(path_to_files+"/" + day_before_file)
    
    countries_by_death = get_countries_dict(covid_data, day_before_data)
    
    top10 = {k: countries_by_death[k] for k in list(countries_by_death)[:10]} 
        
    
    
    print("Analysing data from folder ...\n\n" + 
      "Question 1:\n" +
      "Most recent data is in file '" + recent_file + "'" +
      "\nLast updated at " + latest_last_update +
      "\nTotal worldwide cases: " + str(ww_cases) + " , Total worldwide deaths: " + str(ww_deaths))
    
    print("\nQuestion 2:")
    for i in top10:
        print(i + " - total cases:",top10[i][1], "deaths:", top10[i][0], "new:", top10[i][2])
        
    
    pass

def find_most_recent_file(files_list):
    dates = [i.split('-')[0:2] for i in files_list]
    recent_month = max([i[0] for i in dates])
    recent_day = max([i[1] for i in dates if i[0] == recent_month])
    
    recent_file = files_list[dates.index([recent_month,recent_day])]
    return recent_file


def last_update(data):
    '''
    takes a table of data generated from a covid data file and returns the most recent
    last update

    Parameters
    ----------
    data : pandas Data

    Returns
    -------
    latest_last_update : String

    '''

    # find the most recent update
    Last_Updates = data["Last_Update"]
    
    # convert the last update data to lists of integers to be easier to compare and find most recent
    lu_dates = [int(i.split()[0].replace("-","")) for i in Last_Updates]
    lu_times = [int(i.split()[1].replace(":","")) for i in Last_Updates]
    lu_reformed = [i for i in zip(lu_dates,lu_times)]
    
    # get the times of the most recent date
    lu_only_most_recent_days =[i[1] for i in lu_reformed if i[0] == max(lu_dates)]
    
    idx = lu_times.index(max(lu_only_most_recent_days))
    
    latest_last_update = Last_Updates[idx]
    
    return latest_last_update
    
def get_countries_dict(data, old_data):
    '''
     takes a table of data generated from a covid data file and returns a dictionary with total cases 
     deaths and new cases for each country sorted by number of cases

    Parameters
    ----------
    data : pandas DataFrame

    Returns
    -------
    sorted_dict : dict

    '''
    
    count = dict()

    country_regions_list = data["Country_Region"]
    deaths_list = data["Deaths"] 
    cases_list = data["Confirmed"]
    
    day_before_cases_list = old_data["Confirmed"]
    
    for i in range(len(country_regions_list)):
        country = country_regions_list[i]
        deaths = deaths_list[i] 
        cases = cases_list[i]
        day_before_cases = day_before_cases_list[i]
        
        
        new_cases = cases - day_before_cases
        if country not in count:
            count[country] = [deaths,cases,new_cases]
        else:
            count[country][0] += deaths
            count[country][1] += cases
            count[country][2] += new_cases
            
    sorted_dict = dict(sorted(count.items(), key=lambda item: item[1][1], reverse = True))
    return sorted_dict

        
    
# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    path = '/Users/rishikanair/Desktop/COMP1730/groupassignment'
    # test on folder containg all CSV files
    analyse(path)
    

    
    