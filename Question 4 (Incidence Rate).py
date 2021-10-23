import os
import csv


os.chdir('C:\\Users\\ellaw\\Documents\\ANU\\2021 Semester 2\\comp1730\\Assignments\\Group Ass\\Provided Data\\covid-data')

def sort_files_by_date(path):
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
    import glob
    folder_content = glob.glob('*.csv') #Ensures only csv files are considered

    i=0
    year_month_day = [(int(folder_content[i][6:10]),int(folder_content[i][0:2]),int(folder_content[i][3:5])) for folder_content[i] in folder_content]
    
    sorted_files = tuple(sorted(year_month_day, reverse=True))
    return(sorted_files)
                          
                                                       
    

def select_file(path, i):
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
    directory_contents = sort_files_by_date(path) #To obtain the tuple of sorted files
    selected_file = directory_contents[i]
    file_name = convert_to_file_name_format(selected_file) #Converting to file format
    
    return(file_name)
    



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

################################################################################################

def incidence_rate_and_cfr_dictionary(path):
    '''This function calculates and returns the overall incidence_rate for each country
    This is based on the following calculations:
        Let n=total number of cases, r=the incidence rate, p=population
        Then:
            n = r * (p/100000) [1]
        Therefore:
            p = n/r * 100000  [2]        and            r  = n * 100000 / p  [3]
    For each state or area of a country, the population is found using [2].
    The population of each country is then the sum of the populations of its states
    The total cases for each country was the sum of the total cases for each of its states.
    The incidence rate for the country itself was then calculated using [3]

    Parameters
    ----------
    path : The complete path to the directory containing the files

    Returns
    -------
    sort_by_rate : A list of lists. Each country its own sublist containing the 
    name of the country and the corresponding incidence_rate. The lists are ordered
    in descending order by incidence rate.

    '''
    #Accessing data from the most recent file
    file_name = select_file(path,0)
    file = open(file_name, 'r')
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
    
    #country_and_IR = list(zip(country,incident_rate_per_state))
    
    file.close()
    ##### The dict_of_IR will hold the incident rate (value) for each country (key) 

    #For countries with no breakdown data, we can directly add name:incidence_rate pairs to the dictionary.
    #We define an empty list, 'multiple_states', to record the names of countries with breakdown data for further analysis.
    dict_of_IR = {}
    multiple_states = []
    for i in range(0, len(country)):
        #Breakdown data is unavailable if the country name features just once in the table
        if country.count(country[i]) == 1:
            dict_of_IR[country[i]] = float(incident_rate_per_state[i])
            
       #multiple_states is a list of lists, each list containing country name and incident rate 
        else:
            multiple_states.append([country[i], total_cases_per_state[i], incident_rate_per_state[i], total_deaths_per_state[i]]) 
            
    #### The dict_of_CFR will hold the case_fatality ratio for each country
    dict_of_CFR = {}
    for i in range(0,len(country)):
        if country.count(country[i]) == 1:
            dict_of_CFR[country[i]] = (int(total_deaths_per_state[i])/(int(total_cases_per_state[i])) * 100)
            
      #Creating a dictionary with country name as key and the total deaths as the value
    country_deaths_dict = {}
    for i in range(0,len(multiple_states)):
        if multiple_states[i][0] in country_deaths_dict:
            country_deaths_dict[multiple_states[i][0]] = country_deaths_dict[multiple_states[i][0]] + int(multiple_states[i][3])
        else:
            country_deaths_dict[multiple_states[i][0]] = int(multiple_states[i][3])
    #print(country_deaths_dict)
    
    #We now use the calculations described in the docstring to find the incidence rate for countries with breakdown data.   
    
    #Calculating the population of each state. This is appended to a list such that for each state, the country name and the population of the state are recorded as a sublist.
    population_list = []
    for i in range(0,len(multiple_states)):
        if round(float(multiple_states[i][2]),4) != 0: #Note that if the incidence rate of a state is zero, the calculations are undefined.
            population = int(((int(multiple_states[i][1])) / float(multiple_states[i][2])) * 100000)
            population_list.append([multiple_states[i][0],population])
        
    
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
        CFR = (((Total_cases_in_country)/(Total_cases_in_country))*100)
   
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
             
    return(sort_by_rate)


def Question4_output(path):
    ''' Generates the output of Question 4 from the values calculated in other functions
    Parameters
    ----------
    path : The complete path to the directory where the files are held.
    
    Returns
    -------
    prints a string that displays the name, incidence rate and case_fatality_ratio for the countries with the 10 heighest incident rates.

    '''
    incidence_data = incidence_rate_and_cfr_dictionary(path)
    #case_fatality_data = case_fatality_attempt(path) ## Both of these will be dictionaries
    print("Question 4"+'\n')
    for i in range(0,10):
        country = list(incidence_data.keys())[i]
        rate = int(incidence_data[country][0]) #This gives a whole number of cases per 100000 people, which is mildly easier to comprehend
        case_fatality_ratio = round(float(incidence_data[country][1]),3) #Rounding to 2 decimal places for ease of reading.
        print(country,":", rate,"cases per 100,000 people and case-fatality ratio:",case_fatality_ratio,"%.",'\n')
