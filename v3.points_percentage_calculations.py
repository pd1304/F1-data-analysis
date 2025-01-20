# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:02:02 2024

@author: pareshdokka
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests


races = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\races.csv')
const = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\constructors.csv')
const_results = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\constructor_results.csv')
const_standings = pd.read_csv(r'C:\\Documents\\PYTHON COURSE\\Python F1\\f1db_csv\\constructor_standings.csv')

sprint_2021 = [1061, 1065, 1071]
sprints = [1077, 1084, 1095, 1101, 1107, 1110, 1115, 1116, 1118, 1125, 1126, 1131, 1139, 1141, 1143]

#input constructors name
name = input('Please input the name of the constructor you would like to know about: ') 

#Checks if input for constructor name is valid
while True:
    if name not in const['name'].values: 
        constId = None
        print('Sorry the input is invalid')
        name = input('Please input the name of the constructor you would like to know about: ') 
        
    else:
        # goes through const dataframe to match the name given with its 'constructor_id'
        constId = const.loc[(const.name == name), ['constructorId']]
        # turns the single-celled dataframe with const_id into an integer
        constId_value = constId.values[0][0]
    
        get_lower = int(input('Please insert the year of races you would like from: '))  # lower limit of range
        get_upper = int(input('Please insert the year of races you would like upto: '))
    
        #Checks if input for time range is valid   
        while True:
            if get_lower>get_upper:
                print('Invalid range, Please make sure to give a valid range')
            
                # input the upper and lower ranges for the time period 
                get_lower = int(input('Please insert the year of races you would like from: '))  # lower limit of range
                get_upper = int(input('Please insert the year of races you would like upto: '))  # upper limit of range
            else:
            
                # this is an empty dataframe
                year_races = pd.DataFrame()
    
    
                total_range = list(range(get_lower, get_upper+1))
                for i in total_range:
                    year_races = pd.concat([year_races, races.loc[(races.year == i),['year','raceId']]])
                    # concatinates all the data from year year into one dataframe
    
                race_count = pd.DataFrame(year_races)      
                race_count['year_fraction'] = races['year']+races['round']/races.groupby('year')['round'].transform('max')
    
                raceIds = year_races['raceId']
    
                # all_results: all the results of all the constructors from all the races during the given time range
                all_results = const_results[const_results['raceId'].isin(raceIds)][['raceId','constructorId','points']]
    
                # main_results: results of given constructor from all the races furing the given time range
                main_results = all_results[all_results['constructorId']== constId_value]
                
                final_result = pd.merge(race_count, main_results, on='raceId')
                final_result['max points'] = 0
                
                final_result['max points'] = final_result['year'].apply(lambda x: 25 + 18+1 if 2019 <= x <= 2024 
                                                                        else 25+18 if 2010 <= x <= 2018
                                                                        else 10+8 if 2003 <= x <= 2009
                                                                        else 10+6 if 1991 <= x <= 2002
                                                                        else 9+6 if 1960 <= x <= 1990 
                                                                        else None )
                final_result['max points'] += final_result['raceId'].apply(lambda x: 8+7 if x in sprints
                                                                           else 3+2 if x in sprint_2021
                                                                           else 0)
                final_result['point_percentage'] = final_result['points']/final_result['max points']*100
                
                    
                        
    
    
                #print(all_results) # prints all results
                #print(race_count)
                #print(main_results) # prints results of the particular constructor id
                print(final_result)
                #exit loop
                
                ##PLOT

                x = final_result['year_fraction']
                y = final_result['point_percentage']

                plt.scatter(x,y, marker = 'o')
                plt.xlabel('year')
                plt.ylabel('point percentage')
                plt.show()
                break
        break
    
    