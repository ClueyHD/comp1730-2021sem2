# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 02:32:00 2021

@author: ellaw
"""
import os
import pandas as pd
import csv
import datetime
import fnmatch

def analyse(path_to_files):
    '''Displays the information obtained regarding to Covid-19
    Parameters
    ----------
    path_to_files : The complete path to the directory containing the files.
    Returns
    -------
    Prints the outputs of the constituent functions
    '''
    print("Analysing data from folder",path_to_files,':\n\n')
    Q1(path_to_files)
    Q2(path_to_files)
   # Q3(path_to_files)
    Q4(path_to_files)
    pass
################################################################################################

def sort_files_by_date(path_to_files):
    '''Organises the files in a directory in descending order by their date (year,month,day). 
    Considers only csv files. Returns a tuple containing all csv files such that
    the most recent file is first and the oldest last
    Parameters:
    ----------
            path : The complete path to the desired directory
    Returns:
    -------
            sorted_tuple: A tuple of all csv files, ordered from the latest file to the 
            oldest.
    '''

    files = fnmatch.filter(os.listdir(path_to_files), '*.csv') #Ensures only csv files are considered
    i=0
    year_month_day = [(int(files[i][6:10]),int(files[i][0:2]),int(files[i][3:5])) for files[i] in files]
    
    sorted_files = tuple(sorted(year_month_day, reverse=True))
    return(sorted_files)

def convert_to_file_name_format(file):
    '''Converts the individual segments of a file name (ie the month, day and year)
    into the file name format required
    Parameters
    ----------
            file : A list consisiting of 3 integer elements; the year, month and day
                NOTE: It is assumed that year = file[0] and is of length 4,
                      file[1] is the month and of length <= 2; and file[2]
                      is the day and of length <= 2.
    Returns
    -------
       file_name : A string of the format: mm-dd-YYYY.csv where mm is month, dd is day,
                   and YYYY is year.
    '''
    #Change format of month
    if len(str(file[1])) < 2:
        m = str(0)+str(file[1])
    else:
        m = str(file[1])
    
    #Change format of date
    if len(str(file[2])) < 2:
            d = str(0)+str(file[2])
    else:
            d = str(file[2])
        
    #(Note: we assume the year will always have 4 digits)
    y = str(file[0])
    
    #Arranging into format 'm-d-y.csv'
    file_name = m+'-'+d+'-'+y+'.csv'
    return(file_name)


def select_file(path_to_files, i):
    '''Selects a specific file based on its key in the tuple of sorted files. 
    Converts it from a series of integers to the correct file name format.
    Parameters
    ----------
            path : The complete path to the desired directory
               i : An integer. The index of the wanted file in the tuple.
                    For example; the most recent file is the first entry in the
                   sorted_tuple so i = 0. Similarly, for the oldest file, i=-1.
    Returns
    -------
        file_name : A string. The name of the desired file in the correct format 
                    needed to open it; i.e mm-dd-YYYY.csv
    '''
    directory_contents = sort_files_by_date(path_to_files) #To obtain the tuple of sorted files
    selected_file = directory_contents[i]
    file_name = convert_to_file_name_format(selected_file) #Converting to file format
    
    return(file_name)

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

def incidence_rate_and_cfr_dictionary(path_to_files):
    '''This function calculates and returns the overall incidence_rate for each country and 
    its case-fatality ratio as a percentage
    This is based on the following calculations:
        Incidence Rate:
        Let n=total number of cases, r=the incidence rate, p=population
        Then:
            n = r * (p/100000) [1]
        Therefore:
            p = n/r * 100000  [2]        and            r  = n * 100000 / p  [3]
    For each state or area of a country, the population is found using [2].
    The population of each country is then the sum of the populations of its states
    The total cases for each country was the sum of the total cases for each of its states.
    The incidence rate for the country itself was then calculated using [3]
    
        Case-Fatality-Ratio:
            Let d be the total number of deaths and n be the total cases:
                cfr = d/n * 100 [4]

    Parameters
    ----------
    path_to_files : The complete path to the directory containing the files

    Returns
    -------
    sort_by_rate : A list of lists. Each country its own sublist containing the 
    name of the country and the corresponding incidence_rate. The lists are ordered
    in descending order by incidence rate.

    '''
    #Accessing data from the most recent file. Where there is no incidence rate recorded, the row is ignored.
    file_name = select_file(path_to_files,0)
    file = open(path_to_files+"/" +file_name, 'r')
    with file as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        #For the calculation, we need access to the country name, the total
        #confirmed cases, and the incidence rate. These form the columns of 'data'
        data = [(row[:][3],row[:][7],row[:][8],row[:][12]) for row in reader]
        
    #separating each variable. Where there is no incidence rate recorded, the row is ignored.
    country = [data[:][0] for data in data if data[:][3] != '']
    total_cases_per_state = [data[:][1] for data in data if data[:][3] != '']
    total_deaths_per_state = [data[:][2] for data in data if data[:][3] != '']
    incident_rate_per_state = [data[:][3] for data in data if data[:][3] != '']
    
    
    ##### The dictionary 'dict_of_IR' will hold the incident rate (value) for each country (key) .
        #For countries with no breakdown data, we can directly add (name:incidence_rate) pairs to the dictionary.
    ##### The dictionary 'dict_of_CFR' will hold the case-fatality ratio (value) for each country (key)
        #For countries with no breakdown data, equation [4] can be used directly to calcuate the ratio and update the dictionary.
        #We define an empty list, 'multiple_states', to record the names of countries with breakdown data for further analysis.
    dict_of_IR = {}
    dict_of_CFR = {}
    multiple_states = []
    for i in range(0, len(country)):
        #Breakdown data is unavailable if the country name features just once in the table
        if country.count(country[i]) == 1:
            dict_of_IR[country[i]] = float(incident_rate_per_state[i])
            dict_of_CFR[country[i]] = (int(total_deaths_per_state[i])/(int(total_cases_per_state[i])) * 100)
       
        #multiple_states is a list of lists, each sublist containing country name and incident rate and deaths
        else:
            multiple_states.append([country[i], total_cases_per_state[i], incident_rate_per_state[i], total_deaths_per_state[i]]) 
            
    ###We now use the calculations described in the docstring to find the incidence rate for countries with breakdown data.
    #Calculating the population of each state. This is appended to a list such that for each state, the country name and the population of the state are recorded as a sublist.
    population_list = []
    for i in range(0,len(multiple_states)):
        if round(float(multiple_states[i][2]),4) != 0: #Note that if the incidence rate of a state is zero, the calculations are undefined.
            population = int(((int(multiple_states[i][1])) / float(multiple_states[i][2])) * 100000)
            population_list.append([multiple_states[i][0],population])
            
            
    #Creating a dictionary with country name as key and the total deaths as the value
    country_deaths_dict = {}
    for i in range(0,len(multiple_states)):
        if multiple_states[i][0] in country_deaths_dict:
            country_deaths_dict[multiple_states[i][0]] = country_deaths_dict[multiple_states[i][0]] + int(multiple_states[i][3])
        else:
            country_deaths_dict[multiple_states[i][0]] = int(multiple_states[i][3])
        
    
    #Creating a dictionary with country name as key and population as corresponding value from this list:
        #This involves summing the populations of individual states and is achieved by checking whether a country appears in the dictionary, and if so adding the population of the state to the value; or establishing a key:value pair otherwise.
    country_population_dict = {}
    for i in range(0, len(population_list)):
        if population_list[i][0] in country_population_dict:
            country_population_dict[population_list[i][0]] = country_population_dict[population_list[i][0]] + population_list[i][1]
        else:
            country_population_dict[population_list[i][0]] = population_list[i][1]
    
    #Creating a dictionary with the country name as the key and the total cases as the corresponding value.
    #This was done in a similar way to above, but with the value being directly available from the data for each state.
    country_total_cases_dict = {}
    for i in range(0, len(multiple_states)):
        if multiple_states[i][0] in country_total_cases_dict:
            country_total_cases_dict[multiple_states[i][0]] = country_total_cases_dict[multiple_states[i][0]] + int(multiple_states[i][1])
        else:
            country_total_cases_dict[multiple_states[i][0]] = int(multiple_states[i][1])
    
    #Merging three dictionaries so key is country name and value is [population,cases,deaths]
    country_info_dict = {}
    countries = list(country_total_cases_dict.keys())
    for i in range(0,len(countries)):
            country_info_dict[countries[i]] = [country_population_dict[countries[i]], country_total_cases_dict[countries[i]], country_deaths_dict[countries[i]]]
    
    
    #Applying equation [3] from docstring to determine the overall incidence rate for each country.
    for i in range(0,len(countries)):
        Population_of_country = country_info_dict.get(countries[i])[0]
        Total_cases_in_country = country_info_dict.get(countries[i])[1]
        Overall_incident_rate = ((Total_cases_in_country * 100000) / Population_of_country)
        Total_deaths_in_country = country_info_dict.get(countries[i])[2]
        CFR = (((Total_deaths_in_country)/(Total_cases_in_country))*100)
   
    #We now know the incidence rate for each country and the key:value pairs (country_name:incidence_rate) can be added to the dict_of_IR
        dict_of_IR[countries[i]] = Overall_incident_rate  
        
    #We now know the case-fatality-ratio for each country, and can update dict_of_CFR
        dict_of_CFR[countries[i]] = CFR
    
    
    ### We now sort the data by incidence rate so that the country with the highest incident rate is the first item in the dictionary
    sort_by_rate = dict(sorted(dict_of_IR.items(), key=lambda x:x[1], reverse =True))
    
    #Adding the case_fatality_ratio to each country's value. The value is now of form [incidence_rate, case_fatality_ratio]
    sorted_keys = list(sort_by_rate.keys())
    for i in range(0,len(sorted_keys)):
        sort_by_rate[sorted_keys[i]] = [sort_by_rate[sorted_keys[i]], dict_of_CFR[sorted_keys[i]]]
        ##Please note: Information on how to sort a disctionary based on its values was found at 'Career Karma:How to Sort A Dictionary By Value in Python' Available at: https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
             
    return(sort_by_rate)


def dictionary_of_cases_by_country(path_to_files,recent_file_index,day_before_index):
    '''Generates a dictionary containing information about 

    Parameters
    ----------
    path_to_files : The complete path to the directory containing the files. This is a string
    recent_file_index : The integer corresponding to the index of the most recent file we wish to consider
        in the tuple given by sort_files_by_date function..
        For example, if the most recent file we want to consider is the most recent file overall,
        this value is 0
    day_before_index : The integer corresponding to the index of the file before the recent file
        we wish to consider. That is, day_before_index = recent_file_index + 1

    Returns
    -------
    countries_by_death : A dictionary with the name of a country as a key, and the corresponding value
        being a list of the form [total deaths, total cases, new cases, active cases].

    '''
    # get the data of the most recent file
    recent_file = select_file(path_to_files,recent_file_index)
    covid_data = pd.read_csv(path_to_files+ "/" + recent_file)
    
    # get the data of the second most recent file to find new cases
    day_before_file = select_file(path_to_files,day_before_index) 
    day_before_data = pd.read_csv(path_to_files+"/" + day_before_file)
    
    ##2c
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
    two_weeks_before_file = select_file(path_to_files,14)
    two_weeks_before_data = pd.read_csv(path_to_files + "/" + two_weeks_before_file)
    
    count = dict()

    country_regions_list = covid_data["Country_Region"]
    deaths_list = covid_data["Deaths"] 
    cases_list = covid_data["Confirmed"]
    
    day_before_cases_list = day_before_data["Confirmed"]
    day_before_deaths_list = day_before_data["Deaths"]
    
    two_weeks_before_cases_list = two_weeks_before_data["Confirmed"]
    
    
    # create the dictionary with countries as the keys and the relevant data in a list as the items
    for i in range(len(country_regions_list)):
        country = country_regions_list[i]
        deaths = deaths_list[i] 
        cases = cases_list[i]
        day_before_cases = day_before_cases_list[i]
        day_before_deaths = day_before_deaths_list[i]
        twb_cases = two_weeks_before_cases_list[i]
        
        new_cases = cases - day_before_cases
        new_deaths = deaths - day_before_deaths
        active_cases = cases - twb_cases
        
        if country not in count: # first occurence of country
            count[country] = [deaths, cases, new_cases, new_deaths, active_cases]
        else: # for countries with multiple provinces
            count[country][0] += deaths
            count[country][1] += cases
            count[country][2] += new_cases
            count[country][3] += new_deaths
            count[country][4] += active_cases
            
    # we sort the countries by number of cases in descending order
    countries_by_cases = dict(sorted(count.items(), key=lambda item: item[1][1], reverse = True))
    return countries_by_cases

def sort_and_print_Q2(countries_by_cases):
    '''This takes the dictionary containing the case information for each country, sorts it in descending
    order according to number of cases, and prints the ten countries with the highest cases.'''
    top10 = {k: countries_by_cases[k] for k in list(countries_by_cases)[:10]} 

    for i in top10:
        print(i + " - total cases:",top10[i][1], "deaths:", top10[i][0], "new:", top10[i][2], "active:", top10[i][4])
        
##############################################################################################
def Q1(path_to_files):
    '''This function calculates and returns the answer to question 1 in a format
    that is easily read and interpreted

    Parameters
    ----------
    path_to_files : The complete path to the directory containing the files.

    Returns
    -------
    Prints the Question number, the name of the most recent file and the last recorded update
    as well as the number of cases worldwide and the number of deaths worldwide

    '''
    # Q1a
    
    # find most recent file using the select_file function    
    recent_file = select_file(path_to_files,0)
    covid_data = pd.read_csv(path_to_files+ "/" + recent_file)
    latest_last_update = last_update(covid_data)
    
    # Q1b
    #Calculating the total cases and total deaths worldwide
    ww_cases = sum(covid_data["Confirmed"])
    ww_deaths = sum(covid_data["Deaths"])
    print( 
    "Question 1:\n" +
    "Most recent data is in file '" + recent_file + "'" +
    "\nLast updated at " + latest_last_update +
    "\nTotal worldwide cases: " + str(ww_cases) + ", Total worldwide deaths: " + str(ww_deaths))
    
def Q2(path_to_files):
    '''Calculates and returns information pertaining to the total number of cases, deaths,
    new cases and active cases for each country  as recorded in the most recent file
    Parameters
    ----------
    path_to_files : The complete path to the directory containing the files.

    Returns
    -------
    Prints the question number, and information pertaining to the cases of Covid-19 for the
    ten countries with the highest number of cases.

    '''
    print("\nQuestion 2:")
    
    #Here, the recent_file is the most recent file (select_file(path_to_files,0)), so recent_file_index = 0.
    data = dictionary_of_cases_by_country(path_to_files,0,1)
    
    sort_and_print_Q2(data)
        

def Q3(path_to_files):
    no_of_files = len(sort_files_by_date(path_to_files))
    #Creating a list of the files we want to analyse
    #dates = []
    #for i in range(0,(no_of_files-1)):
        #name = select_file(path_to_files,i)
        #dates.append(name)

    date_cases_deaths_dict = {}
    for i in range(0,(no_of_files - 1)):
        
        case_data = dictionary_of_cases_by_country(path_to_files,i,(i-1))
        new_cases = (list(case_data.values()))[:][2]
        new_deaths = (list(case_data.values()))[:][3]
        total_new_cases = sum(new_cases)
        total_new_deaths = sum(new_deaths)
        date_cases_deaths_dict[i] = [total_new_cases,total_new_deaths]
    
        date = select_file(path_to_files,i).strip(' .csv')
        
        print(date+': new cases:',(date_cases_deaths_dict[i])[0],' new deaths:',(date_cases_deaths_dict[i])[1])
        
        

def Q4(path_to_files):
    ''' Generates the output of Question 4 from the values calculated in other functions
    Parameters
    ----------
    path_to_files : The complete path to the directory containing the files.
    Returns
    -------
    prints a string that displays the name, incidence rate and case_fatality_ratio for the countries with the 10 heighest incident rates.
    '''
    incidence_data = incidence_rate_and_cfr_dictionary(path_to_files)
    #case_fatality_data = case_fatality_attempt(path) ## Both of these will be dictionaries
    print("\n"+"Question 4:")
    for i in range(0,10):
        country = list(incidence_data.keys())[i]
        rate = int(incidence_data[country][0]) #This gives a whole number of cases per 100000 people, which is mildly easier to comprehend
        case_fatality_ratio = round(float(incidence_data[country][1]),3) #Rounding to 2 decimal places for ease of reading.
        print(country,":", rate,"cases per 100,000 people and case-fatality ratio:",case_fatality_ratio,"%.")
        

###############################################################################################
# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.
#if __name__ == '__main__':
    #path_to_files = '.\covid-data'
    # test on folder containg all CSV files
    
#path_to_files = '.\covid-data'    
#analyse(path_to_files)
    
#if __name__ == '__main__':
#   path_to_files = 'C:\\Users\\ellaw\\Documents\\ANU\\2021 Semester 2\\comp1730\\Assignments\\Group Ass\\Provided Data\\covid-data'   
#   #test on folder containg all CSV files#    
#   analyse(path_to_files)
 #   #os.chdir(path_to_files)