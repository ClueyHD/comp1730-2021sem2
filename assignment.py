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
    print("Analysing data from folder ...\n")
    question1(path_to_files)
    question2(path_to_files)
    pass


def question1(path_to_files):
    # Q1a
    unsorted_covid_files_list  = os.listdir(path_to_files)[1:]
    covid_files_list = sort_files_list(unsorted_covid_files_list)
    
    # find most recent file by first finding the latest date, then day    
    recent_file = covid_files_list[-1]
    covid_data = pd.read_csv(path_to_files+ "/" + recent_file)
    latest_last_update = last_update(covid_data)
    
    # Q1b
    ww_cases = sum(covid_data["Confirmed"])
    ww_deaths = sum(covid_data["Deaths"])
    print( 
    "Question 1:\n" +
    "Most recent data is in file '" + recent_file + "'" +
    "\nLast updated at " + latest_last_update +
    "\nTotal worldwide cases: " + str(ww_cases) + ", Total worldwide deaths: " + str(ww_deaths))
        
    pass

def question2(path_to_files):
    print("\nQuestion 2:")
    
    unsorted_covid_files_list  = os.listdir(path_to_files)[1:]
    covid_files_list = sort_files_list(unsorted_covid_files_list)
    
    # get the data of the most recent file
    recent_file = covid_files_list[-1]
    covid_data = pd.read_csv(path_to_files+ "/" + recent_file)
    
    # get the data of the second most recent file to find new cases
    day_before_file = covid_files_list[-2] 
    day_before_data = pd.read_csv(path_to_files+"/" + day_before_file)
    
    # The main assumption we make to estimate active cases is that the recovery time for 
    # Covid-19 is two weeks.  i.e. any actve cases from two weeks before are either recovered or dead.
    # Hence, if we let 
    # T1 = D1 + (A1 + R1) and 
    # T2 = D2 + (A2 + R2)
    # with two weeks in between the total confirmed cases T1 and T2
    # A2 = (A2 + R2) - ((A1 + R1) - (D2 - D1))
    # which simplifies to:
    # A2 = T2 - T1
    # so current active cases is equal to the current confirmed cases minus the confirmed cases from 
    # two wees prior.
    
    # get the data from two weeks before to find active cases
    two_weeks_before_file = covid_files_list[-15]
    two_weeks_before_data = pd.read_csv(path_to_files + "/" + two_weeks_before_file)
    
    count = dict()

    country_regions_list = covid_data["Country_Region"]
    deaths_list = covid_data["Deaths"] 
    cases_list = covid_data["Confirmed"]
    
    day_before_cases_list = day_before_data["Confirmed"]
    
    two_weeks_before_cases_list = two_weeks_before_data["Confirmed"]
    
    
    # create the dictionary with countries as the keys and the relevant data in a list as the items
    for i in range(len(country_regions_list)):
        country = country_regions_list[i]
        deaths = deaths_list[i] 
        cases = cases_list[i]
        day_before_cases = day_before_cases_list[i]
        twb_cases = two_weeks_before_cases_list[i]
        
        new_cases = cases - day_before_cases
        active_cases = cases - twb_cases
        
        if country not in count: # first occurence of country
            count[country] = [deaths, cases, new_cases, active_cases]
        else: # for countries with multiple provinces
            count[country][0] += deaths
            count[country][1] += cases
            count[country][2] += new_cases
            count[country][3] += active_cases
            
    # we sort the countries by number of cases in descending order
    countries_by_death = dict(sorted(count.items(), key=lambda item: item[1][1], reverse = True))
    
    top10 = {k: countries_by_death[k] for k in list(countries_by_death)[:10]} 

    for i in top10:
        print(i + " - total cases:",top10[i][1], "deaths:", top10[i][0], "new:", top10[i][2], "active:", top10[i][3])
        
    pass




def sort_files_list(files_list):    
    dates = [i.split('-')[0:3] for i in files_list]
    
    dif_months = set([i[0] for i in dates])
    
    sorted_files_list = list()
    
    sorted_dates = list()
    
    for m in dif_months:
        one_month = list()
        for n in dates:
            if n[0] == m:
                one_month.append(n)
        sorted_dates.extend(sorted(one_month, key = lambda x: x[1]))
        
    for i in sorted_dates:
        file_name = i[0]+'-'+i[1]+'-'+i[2]
        
        sorted_files_list.append(file_name)
    
    return sorted_files_list


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

    
# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    path = '/Users/rishikanair/Desktop/COMP1730/groupassignment/covid-data'
    # test on folder containg all CSV files
    analyse(path)
    

    
    