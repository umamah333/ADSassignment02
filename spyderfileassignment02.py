# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 11:11:11 2022

@author: umamah
"""

import pandas as pd
import numpy as np
import requests
import seaborn as sns
from IPython.display import display
import matplotlib.pyplot as plt
import datetime as dt

# Base URL used in all the API calls
BASE_URL='http://api.worldbank.org/v2/'

# List of indicators according to the features defined above
INDICATOR_CODES = ['SP.POP.TOTL', 'SP.POP.TOTL.FE.IN', 'SP.POP.TOTL.MA.IN','SP.DYN.CBRT.IN','SP.DYN.CDRT.IN','EG.USE.ELEC.KH.PC', 'EG.FEC.RNEW.ZS' , 'EG.USE.COMM.FO.ZS' ]
country_list=['USA', 'India', 'China', 'Japan', 'Canada', 'Great Britain', 'South Africa']
#renaming the features into the meaningful names
featureMap={
    "SP.POP.TOTL": "Total Population",
    "SP.POP.TOTL.FE.IN": "Female Population",
    "SP.POP.TOTL.MA.IN": "Male Population",
    "SP.DYN.CBRT.IN": "Birth Rate",
    "SP.DYN.CDRT.IN": "Death Rate",
    "EG.USE.ELEC.KH.PC":"Electric Power Consumption(kWH per capita)",
    "EG.FEC.RNEW.ZS":"Renewable Energy Consumption (%)",
    "EG.USE.COMM.FO.ZS":"Fossil Fuel Consumption (%)"
    }
#renaming country codes with their actual names for better understanding
countryMap={
    "US": "USA",
    "IN":"India",
    "CN": "China",
    "JP": "Japan",
    "CA": "Canada",
    "GB": "Great Britain",
    "ZA": "South Africa"
    }
# constant parameters used in sending the request.
params = dict()
# to ensure we receive a JSON response
params['format']='json'
# The data we fetch is for 59 years.
# Hence we change the default page size of 50 to 100 to ensure we need only one API call per feature.
params['per_page']='100'
# Range of years for which the data is needed
params['date']='1960:2018'



# Function to get JSON data from the endpoint
def loadJSONData(country_code): 
    dataList=[]
    
    # iterate over each indicator code specified in the contant INDICATOR_CODES defined above
    for indicator in INDICATOR_CODES: 
        
        # form the URL in the desired format
        # E.g: http://api.worldbank.org/v2/countries/us/indicators/SP.POP.TOTL?format=json&per_page=200&date=1960:2018
        url=BASE_URL+'countries/'+country_code.lower()+'/indicators/'+indicator
        
        # send the request using the resquests module
        response = requests.get(url, params=params)
        
        # validate the response status code
        # The API returns a status_code 200 even for error messages,
        # however, the response body contains a field called "message" that includes the details of the error
        # check if message is not present in the response
        if response.status_code == 200 and ("message" not in response.json()[0].keys()):
            # print("Successfully got data for: " + str(featureMap[indicator]))
            
            # list of values for one feature
            indicatorVals=[]
            
            # the response is an array containing two arrays - [[{page: 1, ...}], [{year: 2018, SP.POP.TOTL: 123455}, ...]]
            # hence we check if the length of the response is >1
            if len(response.json()) > 1:
                
                # if yes, iterate over each object in the response
                 # each object gives one single value for each year
                for obj in response.json()[1]:
                    
                    # check for empty values
                    if obj['value'] == "" or obj['value'] == None:
                        indicatorVals.append(None)
                    else:
                    # if a value is present, add it to the list of indicator values
                        indicatorVals.append(float(obj['value']))
                dataList.append(indicatorVals)
        else:
            # print an error message if the API call failed
            print("Error in Loading the data. Status Code: " + str(response.status_code))
            
    # Once all the features have been obtained, add the values for the "Year"
    # The API returns the indicator values from the most recent year. Hence, we create a list of years in reverse order
    dataList.append([year for year in range(2018, 1959, -1)])
    # return the list of lists of feature values [[val1,val2,val3...], [val1,val2,val3...], [val1,val2,val3...], ...]
    return dataList

#----------------------------------------------------------------------------------------------------
# function to invokde the loadJSONData function and form the final DataFrame for each country
def getCountrywiseDF(country_code):
    
    # The resulting dataframe needs to have meaningful column names
    # hence we create a list of column names from the map defined above
    col_list=list(featureMap.values())
    # append the year column name
    col_list.append('Year')
    
    print("------------------Loading data for: "+countryMap[country_code]+"-----------------------")
    
    # for the given country call the loadJSONData function and fetch the data from the API
    dataList=loadJSONData(country_code)
    
    # transform the list of lists of features into a DataFrame
    # np.column_stack is used to add each list as a column 
    df=pd.DataFrame(np.column_stack(dataList), columns=col_list)
    
    # add the country column by extracting the country name from the map using the country code
    df['Country'] = countryMap[country_code]
    
    # display the resulting dataframe
    display(df.head())
    
    # return the formed dataframe for the given country
    return df




# Call the getCountrywiseDF function with the code of each country under consideration
# We will have a seperate dataframe for each country - 7 data frames
#function call to see the dataframe via countries

US_df=getCountrywiseDF('US')
IN_df=getCountrywiseDF('IN')
CN_df=getCountrywiseDF('CN')
JP_df=getCountrywiseDF('JP')
CA_df=getCountrywiseDF('CA')
GB_df=getCountrywiseDF('GB')
ZA_df=getCountrywiseDF('ZA')

print("Data Loading Completed")



#Data cleaning process from each of the dataframe of the countries

US_df=US_df.dropna()
US_df.head()
print(US_df.describe())
display(US_df)


IN_df=IN_df.dropna()
IN_df.head()
print(IN_df.describe())
display(IN_df)



CN_df=CN_df.dropna()
CN_df.head()
print(CN_df.describe())
display(CN_df)




JP_df=JP_df.dropna()
JP_df.head()
print(JP_df.describe())
display(JP_df)




CA_df=CA_df.dropna()
CA_df.head()
print(CA_df.describe())
display(CA_df)




GB_df=GB_df.dropna()
GB_df.head()
print(GB_df.describe())
display(GB_df)




ZA_df=ZA_df.dropna()
ZA_df.head()
print(ZA_df.describe())
display(ZA_df)

# making list of all countries dataframe to perform concatenation
lst = [US_df,IN_df,CN_df,JP_df,CA_df,GB_df,ZA_df]

df = pd.concat(lst)
df = df.reset_index(drop=True)
df.head()

#converting datatypes explicitly to perform analysis and left year and country as object because they are categorical columns

df["Total Population"] = df["Total Population"].astype("float")
df["Female Population"] = df["Female Population"].astype("float")
df["Male Population"] = df["Male Population"].astype("float")
df["Birth Rate"] = df["Birth Rate"].astype("float")
df["Death Rate"] = df["Death Rate"].astype("float")
df["Electric Power Consumption(kWH per capita)"] = df["Electric Power Consumption(kWH per capita)"].astype("float")
df["Renewable Energy Consumption (%)"] = df["Renewable Energy Consumption (%)"].astype("float")
df["Fossil Fuel Consumption (%)"] = df["Fossil Fuel Consumption (%)"].astype("float")

print(df.dtypes)

#statistical analysis.........

#Heatmap to analyse the correlation between the variables taken

# Exclude the categorical features from the matrix
#df.drop(columns=['Year','Country'], inplace=True, axis=1)


# plot a correlation matrix
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(df.corr(), cmap='RdBu', center=0,ax=ax)
plt.savefig('correlation_us.png')
plt.show()


#lineplot to see the electric power cnsumption of canada as canada is the country of my dataframe with least population



# read the columns from the df for Canada
df=df.loc[100:124, ['Electric Power Consumption(kWH per capita)','Total Population', 'Year']]  

print("First few records of the data: ")
display(df.head())

# line plot
plt.figure(figsize=(6, 5))
plt.title('Total electric power consumption of Canada')
sns.set(style="whitegrid")
plt.ticklabel_format(style = 'plain')
plt.xticks(rotation=60)
sns.lineplot(x='Total Population', y='Electric Power Consumption(kWH per capita)', palette="colorblind",data=df, linewidth=2.5)
