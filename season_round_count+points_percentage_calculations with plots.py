# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:02:02 2024

@author: pareshdokka
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


# Import excel files 
races = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\races.csv')
const = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\constructors.csv')
const_results = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\constructor_results.csv')
const_standings = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\constructor_standings.csv')

#Sprint information:
sprint_2021 = [1061, 1065, 1071]
sprints = [1077, 1084, 1095, 1101, 1107, 1110, 1115, 1116, 1118, 1125, 1126, 1131, 1139, 1141, 1143]



#input constructors name
name = input('Please input the name of the constructor you would like to know about: ') 

# VERIFICATION
# In this section we verify whether the given inputs are valid or not. 

#Checks if input for constructor name is valid
while True:
    if name not in const['name'].values: 
        constId = None
        print('Sorry the input is invalid')
        name = input('Please input the name of the constructor you would like to know about: ') 
        
    else:
        # goes through const dataframe to match the name given with its 'constructor_id'
        constId = const.loc[(const.name == name), ['constructorId']]
        
        #Currently constId gives out a single celled dataframe. Instead, we want the value within the cell as an integer
        #To do so, we can simply use .values[x][y], and specify the row and column number to extract the value in that
        #particular cell. Assign the value to a variable 'constId_value' and there you have it.
        constId_value = constId.values[0][0]
    
        get_lower = int(input('Please insert the year of races you would like from: '))  # lower limit of range
        get_upper = int(input('Please insert the year of races you would like upto: '))  # upper limit of range
    
        #Checks if input for time range is valid   
        while True:
            if get_lower>get_upper:
                print('Invalid range, Please make sure to give a valid range')
            
                # input the upper and lower ranges for the time period 
                get_lower = int(input('Please insert the year of races you would like from: '))  # lower limit of range
                get_upper = int(input('Please insert the year of races you would like upto: '))  # upper limit of range
            else:
                # not the best way to go about the input validation. The entire main code is under this else statement.
                
                
                ##############
                # RACES EXTRACTION FROM GIVEN INPUTS
                # in this section, a dataframe is created with all the races included in the given time range
              
                # This is an empty dataframe that has been created. Soon it will be filled 
                year_races = pd.DataFrame()
                
                # total_range: makes alist of all the values between the input limits
                total_range = list(range(get_lower, get_upper+1))
                
                for i in total_range:
                    year_races = pd.concat([year_races, races.loc[(races.year == i),['year','raceId']]])
                    # concatinates all the data from year year into one dataframe
                    # .loc is used to go through each i in total_range and find the matches in races file.
                    # .concat is used to take the matches and add it to year_races (the earlier empty dataframe)
                    # Only 'year' and 'raceId' columns are added to year_races dataframe 
                ###############
                
                
                
                ###############
                # MAPPING ROUNDS/ SEASONS
                # In this section, a database is created which contains every round as a fraction of their respective year.
                # eg. 2021 has 21 races, hence, each race will progress fractionally (2021.xx ), until the last race jumpts to 2022.00
                # This is currently just the year_races dataframe that has been created. We could have used the same dataframe, but this more clarifying for me personally
                race_count = pd.DataFrame(year_races)
                
                # A column 'year_fraction' is introduced
                race_count['year_fraction'] = races['year']+races['round']/races.groupby('year')['round'].transform('max')
                # races.groupby('year')['round'] groups all the rounds in a season together
                # Applying .transform('max') gives us the length of this group, or in other words, No.rounds in that year 
                #Eg: for 2021, it groups all races, and outputs the length of the group which is: 21. Hence there are 21 races in the year 2021
                # So overall, we get: YEAR + ROUND/NO.ROUNDS
                #################
                
                
                #################
                # CONSTRUCTOR RESULT EXTRACTION FROM EACH RACE
                # Earlier, we extracted races that are within the input time range.
                # In this section, we extract the results from each race of the input Constructor
                
                # A dataframe with raceIds of the valid races.
                raceIds = year_races['raceId']
    
                # all_const_results: all the results of all the constructors from all the races during the given time range
                all_const_results = const_results[const_results['raceId'].isin(raceIds)][['raceId','constructorId','points']]
                # const_results['raceId'].isin(raceIds) checks for our raceIds in const_results file
                #.isin() checks if value is in a specified list or not, and returens True or False.
                
                # chosen_const_results: results of given constructor from all the races during the given time range
                chosen_const_results = all_const_results[all_const_results['constructorId']== constId_value]
                # Further filter out the results, to remove any results that rae not of the unput constructors
                
                # New dataframe whcih merges the race_count and chosen_const_results
                final_result = pd.merge(race_count, chosen_const_results, on='raceId')
                # on= 'raceId' uses the column raceId which is common in both dataframes to merge them
                #################
                
                
                #################
                # POINT CALCULATION
                #In this sectin we will calculate the points for each result as a fraction of max points
                
                #Introduce a column 'max points'
                final_result['max points'] = 0
                
                #Apply a function to the column for max points a team could get over the years
                #Uses the 'year' column to apply the lambda function, and get out the max points
                final_result['max points'] = final_result['year'].apply(lambda x: 25 + 18+1 if 2019 <= x <= 2024 
                                                                        else 25+18 if 2010 <= x <= 2018
                                                                        else 10+8 if 2003 <= x <= 2009
                                                                        else 10+6 if 1991 <= x <= 2002
                                                                        else 9+6 if 1960 <= x <= 1990 
                                                                        else None )
                
                #Add the sprint races points
                final_result['max points'] += final_result['raceId'].apply(lambda x: 8+7 if x in sprints
                                                                           else 3+2 if x in sprint_2021
                                                                           else 0)
                
                #Introduce new column that gives max points as a percentage. This is the column that will be 
                #plot in the Y-axis
                final_result['point_percentage'] = final_result['points']/final_result['max points']*100
                ###################
                    
                        
    
                ###################
                #CHECKS
                #In this section each dataframe is printed to check if all the info is accurate or not.
                '''
                print(all_const_results) # prints all results
                print(race_count)
                print(chosen_const_results) # prints results of the particular constructor id
                '''
                print(final_result)
                ###################
                
                
                
                ###################
                #PLOT
                # In this section we plot our results to get a graph with the year_fraction in x-axis and point_percentage in the y-axis.
                x = final_result['year_fraction']
                y = final_result['point_percentage']

                plt.scatter(x,y, marker = 'o')
                plt.xlabel('year')
                plt.ylabel('point percentage')
                plt.show()
                break
        break
    
    