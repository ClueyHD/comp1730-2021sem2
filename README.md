# comp1730-2021sem2
COMP1730 Group Assignment

COMP1730/6730 Project Assignment
As we all know the current COVID-19 pandemic has caused a massive impact around the world. It is perhaps the most severe disease in the modern human history: hundreds of millions of people have been infected by SARS-CoV-2 (the coronavirus that causes COVID-19) and millions died.

In an effort to keep track of the global infection, the Center of Systems Science and Engineering at Johns Hopkins University (USA) has maintained a public data source that updates the total cases and deaths for every affected country/region on a daily basis. In this assignment, you will write a python program to analyse this data and to answer some questions about COVID-19.

Practical information
The assignment is due on Monday the 25th of October at 9:00am, Canberra time (the beginning of semester week 12). Like all other due dates, this deadline is hard: late submissions will NOT be accepted.

For this assignment, you may work in groups of up to three students. Working in larger groups (more than three students) is not allowed. If there is an indication of four or more students working together, or sharing parts of solutions, all students involved will have to be investigated for possible plagiarism.

A group sign-up activity on wattle is available until the 11th of October at 9:00am (Monday of semester week 10). If you intend to work in a group, you and your team mates should find a free group and add yourselves to it. (The group numbers have no meaning; we only care about which students are in the same group.)

Working in a group is not required. If you want to do the assignment on your own, please add yourself to the “I want to do the assignment on my own” group, so that we can keep track. Remember that deadline extensions can only ever be given to individuals, not to groups. If you choose to work in a group, it is your responsibility to organise your work so that it cannot be held up by the unexpected absence of one group member.

Each student must submit two files:

Their code (a python file). For students working in a group, it is required that all students in the group submit identical code files.
An individual report, with answers to a set of questions. Details about the format of the report and the questions are in the section Questions for the individual report below.
Data and files provided
The data for COVID-19 cases and deaths have been collected on a daily basis. We provide zip file with a number of CSV files:

covid-data.zip
Unzipping this file will create a folder covid-data containing the CSV data files. Each CSV file is named MM-DD-YYYY.csv, and contains the statistics up to that day for every country or region in the world with at least one recorded case. For many countries/regions, the statistics are broken down into states/provinces. For example, within Australia we have data for each state and territory (such as “Australian Capital Territory”, “Victoria”, etc). For the US, the data is even further broken down into Counties.

Each MM-DD-YYYY.csv file has a header line with names of the columns (see below). The following lines contain actual data. The meanings of the columns are:

FIPS: US only. Federal Information Processing Standards code that uniquely identifies counties within the USA. For other countries/regions, this column will be empty.
Admin2: County name. US only. For other countries/regions, this column will be empty.
Province_State: Province, state or dependency name for those countries/regions that we have breakdowns per state/province (e.g. Australia, China, Germany, etc.). For other countries without such a breakdown, this column will be empty.
Country_Region: Country, region or sovereignty name. The names of locations correspond with the official designations used by the U.S. Department of State.
Last_Update: Last time that the entry was updated, in the format YYYY-MM-DD HH:mm:ss (24 hour format, in UTC).
Lat and Long_: Dot locations on the dashboard. All points (except for Australia) shown on the map are based on geographic centroids, and are not representative of a specific address, building or any location at a spatial scale finer than a province/state. Australian dots are located at the centroid of the largest city in each state.
Confirmed: Total number of confirmed (positive) cases up to the corresponding day shown in the CSV file name.
Deaths: Total number of deaths up to the corresponding day shown in the CSV file name.
Recovered: Total recovered cases. However, this field is no longer updated due to the unreliability of the data source. Therefore, you can assume that this column will be empty for all lines in the CSV file. It is just still there for compatibility of older versions of the data.
Active: Active cases = total cases - total recovered - total deaths. However, this field is no longer updated due to the unreliability of the data source. Therefore, you can assume that this column will be empty for all lines in the CSV file. It is just still there for compatibility of older versions of the data.
Combined_key: combined name in the format "Province_State, Country_Region" (for US this will be "Admin2, Province_State, Country_Region"). For those countries without breakdowns, Combined_Key is equal to Country_Region. Combined_key will be distinct for different lines of the file. That’s why it’s called a “key”.
Incident_Rate: Total number of all cases to date per 100,000 people.
Case_Fatality_Ratio: Number of deaths divided by number of cases in percentage. That means, this value is equal to Deaths / Confirmed * 100%.
As an example, let’s look at this one line in 09-14-2021.csv:

,,Australian Capital Territory,Australia,2021-09-15 03:22:37,-35.4735,149.0124,665,3,,,"Australian Capital Territory, Australia",155.33753795842094,0.45112781954887216
This means that until Sept 14th 2021, in the state Australian Capital Territory of the country Australia, there are a total of 665 COVID-19 cases from the beginning of the pandemic (column Confirmed), 3 among them are dead (column Deaths); on average there are 155.33 confirmed cases out of 100,000 people (column Incident_Rate); 0.45% of infected people are dead (column Case_Fatality_Ratio, which should be equal to Deaths divided by Confirmed * 100%). This record was updated on 2021-09-15 03:22:37, UTC time.

If you’re interested, you can find the original data files on the GitHub repository of Johns Hopkins University.

For information and examples of how to read and process CSV files, see Lab 6.

Here, you can safely assume that:

In that folder there will be at least 30 CSV files for 30 consecutive days up to a certain last date. However, the last date may change. For example, when we test your assignment, we may add new data.

All CSV files will have the same header line and the same number of lines (records). Moreover, the order of the lines stay the same.

Between any 2 CSV files, the only columns that might be different are Last_Updated, Confirmed, Deaths, Incident_Rate, and Case_Fatality_Ratio. All other columns will remain the same line-by-line.

Questions for analysis (code)
A template file for the assignment code is provided here:

assignment.py
In this file, there is only one function that you must implement: analyse(path_to_files). The function takes one argument, which is the complete path to the directory containing the data files that it should read and analyse. You can assume that the argument is a string. The function should print out the results of the analysis. It does not have to return any value. The specific questions that your analysis should answer are described below. The following are some general requirements and things to keep in mind:

You do not have to solve all the questions, but you can only gain marks for the ones that you have attempted (see Marking criteria below for details on how we will mark your submission).
Although we do not specify the exact format in which you should print the results of the analysis, you should make it easy for the user (and marker) to see what is being shown. Ease of reading the output of your program is part of the marking criteria.
Although there is only one function in the assignment template that you must implement, you can define other functions and use them in your solution. Indeed, good code organisation, including appropriate use of functional decomposition, is part of the marking criteria.
Question 1(a): Finding the CSV file with the most recent date
Among all the MM-DD-YYYY.csv files in the provided folder, find which file corresponds to the most recent date by its name. From this file, find out the exact timestamp of the last record being updated. Note that the last update time might be different for different rows and that the last update time may not be from last row of the data file. Print the result like this:

Analysing data from folder ...

Question 1:
Most recent data is in file `MM-DD-YYYY.csv`
Last updated at YYYY-MM-DD HH:mm:ss
Hint: You can use the function listdir from the os module to get a list of all the files in the data directory.

Question 1(b): Total worldwide cases and deaths
From this most recent file, report the total number of cases and deaths worldwide. Print the result like this:

Analysing data from folder ...

Question 1:
Most recent data is in file `MM-DD-YYYY.csv`
Last updated at YYYY-MM-DD HH:mm:ss
Total worldwide cases: ... , Total worldwide deaths: ...
Question 2(a): Total cases and deaths by country
For every country in the world, calculate the total number of confirmed cases and deaths in that country from the most recent CSV file. Sort the countries in descending order of number of cases, and print the top 10 (so that the country with the most cases is printed first). Print the results with one line per country, for example like this:

Analysing data from folder ...

Question 1:
...

Question 2:
US - total cases: ... deaths: ...
India - total cases: ... deaths: ...
Brazil - total cases: ... deaths: ...
...
Question 2(b): New cases by country
For every country, compute the number of new cases during the one day immediately before the last update. That is, extend the output for the top-10 countries to something like:

Analysing data from folder ...

Question 1:
...

Question 2:
US - total cases: ... deaths: ... new: ...
India - total cases: ... deaths: ... new: ...
Brazil - total cases: ... deaths: ... new: ...
...
For this question, it is important that you document how you calculate the new case. Use comments and docstrings (as appropriate) in your assignment code.

Question 2(c): Active cases by country
The numbers of active cases are an important information for public health decisions. Theoretically for any day t, we have total_cases[t] = deaths[t] + active[t] + recovered[t]. However, the data files only keep track of total_cases[t] and deaths[t]. Therefore, active[t] and recovered[t] are unknown although we know the sum.

From the data files provided, you now need to estimate the currently active cases per country. Extend the output to something like this:

Analysing data from folder ...

Question 1:
...

Question 2:
US - total cases: ... deaths: ... new: ... active: ...
India - total cases: ... deaths: ... new: ... active: ...
Brazil - total cases: ... deaths: ... new: ... active: ...
...
It’s OK to report a possible range for active cases if an exact number can’t be estimated. For this question, it is important that you document how you estimate the active cases, and any assumptions that you have made. Use comments and docstrings (as appropriate) in your assignment code.

Question 3(a): Daily cases and deaths
Report the worldwide number of new daily cases and new daily deaths for each of the days that you can find from the data files, except for the oldest day. Print the results with one line per day in reverse chronological order, for example like this:

Analysing data from folder ...

Question 1:
...

Question 2:
...

Question 3:
2021-09-14 : new cases: ...   new deaths: ...
2021-09-13 : new cases: ...   new deaths: ...
2021-09-12 : new cases: ...   new deaths: ...
...
Question 3(b): Weekly cases and deaths
The daily cases tend to have a bias towards lower number for the weekend. That means, the number of new cases for Saturday and Sunday tend to be lower than the weekdays, likely due to reduced testing activities during the weekend.

Therefore, we want to summarise the number of new cases and deaths on a weekly basis to have a more stable statistic. Report the number of new weekly cases and deaths up to the most recent date, where a week is defined from Monday to Sunday. Note that for the last week in our data the ending day might not be a Sunday. Likewise, for the first week in the data the starting day might not be a Monday. Print the results like this:

Analysing data from folder ...

Question 1:
...

Question 2:
...

Question 3:
2021-09-14 : new cases: ...   new deaths: ...
2021-09-13 : new cases: ...   new deaths: ...
2021-09-12 : new cases: ...   new deaths: ...
...

Week 2021-09-13 to 2021-09-14 : new cases: ...  new deaths: ...
Week 2021-09-06 to 2021-09-12 : new cases: ...  new deaths: ...
Week 2021-08-30 to 2021-09-05 : new cases: ...  new deaths: ...
...

Question 4: Incident Rate
Each row in the data file shows the incident rate: the number of cases per 100,000 people in a local area. For a country without breakdown data (i.e., without cases per state/province or counties), we then directly know the incident rate of that country from the data file. For other countries with breakdown data (e.g., US, Australia, etc.), we don’t know the incident rate of these countries directly from the data files.

From the data in the most recent CSV file, calculate the incident rate per country and the case-fatality ratio for that country (number recorded deaths / number cases in percentage). You can ignore those rows where Incident_Rate is empty. Note that the country with the highest total number of cases is not necessarily the country with the highest incident rate because they have different populations. Print the top-10 countries in terms of incident rate in descending order, such that the top-1 country is printed first. Print the results with one line per country, for example like this:

Analysing data from folder ...
    
Question 1:
...
    
Question 2:
...

Question 3:
...
    
Question 4:
Seychelles : ... cases per 100,000 people and case-fatality ratio: ... %
Montenegro : ... cases per 100,000 people and case-fatality ratio: ... %
Andorra : ... cases per 100,000 people and case-fatality ratio: ... %
...
Again, for this question, it is important that you document how you calculate these numbers, and any assumptions that you have made. Note that you don’t need to use any external information such as about the population data of the countries. The answers for this question can be fully determined from the data files provided. Use comments and docstrings (as appropriate) in your assignment code.

Questions for the individual report
A template for your report is provided here:

assignment_report.txt
The template is a plain text file; write your answers where indicated in this file. Do not convert it to doc, docx or any other format.

The questions for you to answer in the report are:

Report question 1: Write your name and ANU ID.
Report question 2: If you are part of a group, write the names and ANU IDs of ALL members of this group. If you are doing the assignment on your own (not part of a group), just write “not part of a group”.
Report question 3: Select a piece of code in your assignment solution that you have written, and explain:

(a) What does this piece of code do?

(b) How does it work?

(c) What other possible ways did you consider to implement this functionality, and why did you choose the one you did?

For this question, you should choose a piece of code of reasonable size and complexity. If your code has an appropriate level of functional decomposition, then a single function is likely to be a suitable choice, but it can also be a part of a function. It should not be something trivial (like a single line, or a simple loop).

For all parts of this question, it is important that your answers are at an appropriate level of detail. For part (a), describe the purpose of the code, including assumptions and restrictions. For parts (b) and (c), provide a high-level description of the algorithmic idea (and alternative ideas), not a line-by-line description of each statement.

There is no hard limit on how short or how long your answer can be, but an answer that is short and clear answer is always better than one that is long and confusing, if both of them convey the same essential information. As a rough guideline, an appropriate answer may be about 100 - 300 words for each of parts (a) - (c).

Submission requirements
Every student must submit two files: Your assignment code (assignment.py) and your individual report (assignment_report.txt). An assignment submission link will be available on wattle shortly after the assignment specification is released.

Restrictions on code
There are certain restrictions on your code:

You should NOT use any global variables or code outside of functions, except for the test cases in the if __name__ == '__main__' section. You can add other test cases in the main section if you wish.
You can import modules that you find useful. However, we will test your code using the Anaconda distribution of python, so only modules available in Anaconda can be used. If in doubt about whether a module can be used, post a question to the wattle discussion forum before you decide to use it.
The argument to the analyse function is the path to the folder containing files to analyse. You must only read files in this folder. You must NOT write any file, or use any of the functions of the os module (such as changing the working directory) other than listdir.
It is very important that you follow these restrictions. If you do not, we may not be able to test your code, in which case you can not gain any marks for code functionality.

Assumptions
We will test your code with CSV files other than those provided above. All input files will follow the same format, i.e., they will be CSV files, and have the same columns (in the same order) with the same content format, as described above (see Data and files provided). However, they will contain different data. For example, data files we provide range over a specific set of dates. You should not assume this will always be the case. The number and names of countries or regions differ, or the range of dates present in the folder may be different.

Referencing
In the course of solving the assignment problem, you will probably want to make use of all sources of knowledge available: the course materials, text books, on-line python documentation, and other help that you can find on-line. This is all allowed. However, keep in mind that:

If you find a piece of code, or an algorithmic idea that you implement, somewhere on-line, or in a book or other material, you must reference it. Include the URL where you found it, the title of the book, or whatever is needed for us to find the source, and explain how you have used it in an appropriate place in your code (docstring or comment).

Although you can often find helpful information in on-line forums (like stackexchange, for example), you may not use them to ask questions that are specific to the assignment. Asking someone else to solve an assignment problem for you, whether it is in a public forum or in private, is a form of plagiarism, and if we find any indication that this may have occurred, we will be forced to investigate.

If you have any doubt about if a question is ok to ask or not, you can always post your question to the wattle discussion forum. We will answer it at a level of detail that is appropriate.

Remember that:

Working in groups of more than three students is not allowed. While you may develop your solution (python code) in a group of up to three students, you may not share your solution, or parts of your solution, with, or receive parts of a solution from, anyone outside this group.

The individual report must be done by you yourself. The other members of your group may not assist you with it.

Marking criteria
The code component accounts for 95% of the total assignment marks, and your individual report for the remaining 5%. For the questions of the code component, the breakdown is as follows:

Q1(a): 10%
Q1(b): 20%
Q2(a): 10%
Q2(b): 10%
Q2(c): 20%
Q3(a): 5%
Q3(b): 10%
Q4: 10%
Your code will be marked on two criteria: Functionality and code quality. The division of marks between them is 60% for functionality and 40% for code quality. We will also consider the efficiency of your code. Efficiency is part of both functionality and code quality.

Functionality encompasses code running without error on input files that follow the same format as the example files provided, and produces an output that is easy to understand and correct. Examples of increasing levels of functionality are:

Code runs without runtime error, and in a reasonable amount of time, on the provided example data files.
The output is understandable, and includes the information that is asked for in the question.
The output is correct for some of the provided example data files.
The output is correct for all of the provided example data files.
Code runs without runtime error, and in a reasonable amount of time, on other data files that follow the specified format.
The output is correct for other data files as well.
We do not specify a precise limit for what is “a reasonable amount of time”, but as a guide, your code should process the example data files in no more than a minute or two. If it takes much longer, then we will not be able to test your code fully, which is practically the same as it not running at all.

Code quality includes the aspects that we have discussed in lectures and homeworks:

Good code documentation. This includes appropriate use of docstrings and comments.
Remember that for some questions you will have to make some assumptions, and decisions how to calculate your estimate. You should describe these in the code, using docstrings and comments as appropriate.
Good naming. This includes variable and function names.
Good code organisation, including appropriate use of functional decomposition. Remember that even though the assignment template has only one function that you must implement, you can define other functions and use them in your solution.
Efficiency. This includes things like considering the complexity of the operations that you use, and avoiding unnecessarily slow methods of doing things. We do not require that every part is implemented in an optimally efficient way, but code that has many or large inefficiencies is considered to have lower quality.

https://cs.anu.edu.au/courses/comp1730/assessment/project/

