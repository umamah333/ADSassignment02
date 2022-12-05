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
INDICATOR_CODES = ['SP.POP.TOTL', 'SP.POP.TOTL.FE.IN', 'SP.POP.TOTL.MA.IN','SP.DYN.CBRT.IN','SP.DYN.CDRT.IN','EG.USE.ELEC.KH.PC', 'EG.FEC.RNEW.ZS' , 'EG.USE.COMM.FO.ZS' , 'SL.IND.EMPL.ZS' , 'SL.AGR.EMPL.ZS' , 'NY.GDP.MKTP.CD' ]
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
    "EG.USE.COMM.FO.ZS":"Fossil Fuel Consumption (%)",
    "SL.IND.EMPL.ZS":"Employment in Industry(%)",
    "SL.AGR.EMPL.ZS": "Employment in Agriculture(%)",
    "NY.GDP.MKTP.CD": "GDP in USD"
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
df["Employment in Industry(%)"] = df["Employment in Industry(%)"].astype("float")
df["GDP in USD"] = df["GDP in USD"].astype("float")
df["Employment in Agriculture(%)"] = df["Employment in Agriculture(%)"].astype("float")
pd.to_datetime(df.Year, format='%Y')

print(df.dtypes)


#statistical analysis.........

#Heatmap to analyse the correlation between the variables taken

# Exclude the categorical features from the matrix
#df.drop(columns=['Year','Country'], inplace=True, axis=1)


# plot a correlation matrix
fig, ax = plt.subplots(figsize=(10,10))
plt.title('correlation matrix of the indicators')
sns.heatmap(df.corr(), cmap='RdBu', center=0,ax=ax)
plt.savefig('correlation_us.png')
plt.show()


#lineplot to see the electric power cnsumption of canada as canada is the country of my dataframe with least population



# read the columns from the df for Canada
df=df.loc[96:119, ['Electric Power Consumption(kWH per capita)','Total Population', 'Year']]  

print("First few records of the data: ")
display(df.head())

# line plot
plt.figure(figsize=(6, 5))
plt.title('Total electric power consumption of Canada')
sns.set(style="whitegrid")
plt.ticklabel_format(style = 'plain')
plt.xticks(rotation=60)
plt.savefig('Electric power usage canada.png')
sns.lineplot(x='Total Population', y='Electric Power Consumption(kWH per capita)', palette="colorblind",data=df, linewidth=2.5)


#Electric power consumption of India and China

# function to extract specific columns from the DFs for India and China
def form_in_cn_df():
    # for India
    indf=IN_df[['Total Population', 'Electric Power Consumption(kWH per capita)', 'Country']]
    # for China
    cndf=CN_df[['Total Population', 'Electric Power Consumption(kWH per capita)', 'Country']]
    # combine the two dataframes
    in_cn_df=pd.concat([indf, cndf])
    return in_cn_df

# get the desired data
in_cn_df=form_in_cn_df()
print("Few records from the selected features: ")
display(in_cn_df.head())

# scatter plot
plt.figure(figsize=(7, 5))
plt.ticklabel_format(style = 'plain')
plt.title('Electric consumption:India V/S Canada')
plt.xticks(rotation=60)
sns.set(style="whitegrid")
plt.savefig('india china E.power usage graph.png')
ax=sns.scatterplot(x='Total Population', y='Electric Power Consumption(kWH per capita)', hue='Country', palette="bright", data=in_cn_df)



#comparison of all the seven countries birth and death rate taken for analysis
df1 = pd.DataFrame(columns = ['birthrates', 'deathrates', 'countries'], 
                   index = [])
print(df1)

usa=US_df['Birth Rate'].mean().round(2),US_df['Death Rate'].mean().round(2)
usa=np.asarray(usa)

india=IN_df['Birth Rate'].mean().round(2),IN_df['Death Rate'].mean().round(2)
india=np.asarray(india)

china=CN_df['Birth Rate'].mean().round(2),CN_df['Death Rate'].mean().round(2)
china=np.asarray(china)

JP=JP_df['Birth Rate'].mean().round(2),JP_df['Death Rate'].mean().round(2)
JP=np.asarray(JP)

Canada=CA_df['Birth Rate'].mean().round(2),CA_df['Death Rate'].mean().round(2)
Canada=np.asarray(Canada)

GB=GB_df['Birth Rate'].mean().round(2),GB_df['Death Rate'].mean().round(2)
GB=np.asarray(GB)

ZA=ZA_df['Birth Rate'].mean().round(2),ZA_df['Death Rate'].mean().round(2)
ZA=np.asarray(ZA)



df1.loc[0,:]=[usa[0],usa[1],'USA']
df1.loc[1,:]=[india[0],india[1],'India']
df1.loc[2,:]=[china[0],china[1],'China']
df1.loc[3,:]=[JP[0],JP[1],'JAPAN']
df1.loc[4,:]=[Canada[0],Canada[1],'Canada']
df1.loc[5,:]=[GB[0],GB[1],'Great Britain']
df1.loc[6,:]=[ZA[0],ZA[1],'South Africa']
print(df1)



#plotting a group barplot to view the average birth and death rate of each of the countries selected
plt.figure(figsize=(7, 5))
# plot the chart using matplotlib.pyplot library

df1.plot(kind='bar',x='countries',y=['birthrates','deathrates'])
plt.title('Average birthrate and deathrate of the countries')
plt.savefig('avg birth and deathrates.png')
plt.show()

#extracting Great Britain data from the complete dataframe to show the Energy consumption of the Great Britain


#extracting Great Britain data from the complete dataframe to show the Energy consumption of the Great Britain upto 2010
plt.plot(GB_df.loc[4:, ['Year']],GB_df.loc[4:, ['Electric Power Consumption(kWH per capita)']],'.-')
plt.plot(GB_df.loc[4:, ['Year']],GB_df.loc[4:, ['Renewable Energy Consumption (%)']],'.-')
plt.plot(GB_df.loc[4:, ['Year']],GB_df.loc[4:, ['Fossil Fuel Consumption (%)']],'.-')

plt.legend(['Electric Power Consumption(kWH per capita)', 'Renewable Energy Consumption(%)', 'Fossil Fuel Consumption(%)'], loc='best')
plt.title("Energy Consumption in Great Britian\n")
plt.xlabel('Year')
plt.ylabel('Energy Consumption')
plt.xticks(rotation=60)
plt.savefig('GB energy consumption.png')
plt.show()


# function to extract specific columns from the DFs of all countries

# for India
indf=IN_df[['Total Population','Country','Year']]
    
# for China
chinadf=CN_df[['Total Population', 'Country','Year']]
#for USA
usadf=US_df[['Total Population', 'Country','Year']]
#for great britain
gbdf=GB_df[['Total Population','Country','Year']]
#for canada
candf=CA_df[['Total Population','Country','Year']]
#for south africa
southdf=ZA_df[['Total Population','Country','Year']]
#for Japan
japdf=JP_df[['Total Population','Country','Year']]
# combine the two dataframes
lst=[indf,chinadf,usadf,gbdf,candf,southdf,japdf]
df6 = pd.concat(lst)
df6=pd.DataFrame(df6)
df6=df6.reset_index(drop=True)


df2000 = df6[df6["Year"] == 2000]
df2000.rename(columns={'Total Population':'T.pop in 2000'}, inplace=True)
df2000.drop('Year', inplace=True, axis=1)
df2000=df2000.reset_index(drop=True)
print(df2000)

df2010 = df6[df6["Year"] == 2010]
df2010.rename(columns={'Total Population':'T.pop in 2010'}, inplace=True)
df2010.drop('Year', inplace=True, axis=1)
df2010=df2010.reset_index(drop=True)
df2010.head()


df_merged = df2000.merge(df2010)
print('Result:\n', df_merged)

#after finding total population for the years 2000 and 2010 now we will visualise
# it graphically to see the difference of the population in 10 years

plt.figure(figsize=(7, 5))
# plot the chart using matplotlib.pyplot library
df_merged.plot(kind='bar',x='Country',y=['T.pop in 2000','T.pop in 2010'],color=['red', 'green'])
plt.title('Population comparison in 2000 and 2010')
plt.savefig('total population comparison.png')

#extracting the gdp for last 10 years
# function to extract specific columns from the DFs of all countries

# for India
indfg=IN_df[['GDP in USD','Country','Year']]
    
# for China
chinadfg=CN_df[['GDP in USD', 'Country','Year']]
#for USA
usadfg=US_df[['GDP in USD', 'Country','Year']]
#for great britain
gbdfg=GB_df[['GDP in USD','Country','Year']]
#for canada
candfg=CA_df[['GDP in USD','Country','Year']]
#for south africa
southdfg=ZA_df[['GDP in USD','Country','Year']]
#for Japan
japdfg=JP_df[['GDP in USD','Country','Year']]
# combine the two dataframes
lstg=[indfg,chinadfg,usadfg,gbdfg,candfg,southdfg,japdfg]
df6g = pd.concat(lstg)
df6g = pd.DataFrame(df6g)
df6g = df6g.reset_index(drop=True)
df6g = df6g[df6g.Year >= 2004]
df6g.head(40)

# set figure size
plt.figure(figsize=(7, 5))
sns.set(style="whitegrid")
plt.title('GDP in2012')
# plot using seaborn library
ax=sns.lineplot(x='Year', y='GDP in USD', hue='Country', style="Country",palette="Set2", markers=True, dashes=False, data=df6g, linewidth=2.5)
plt.savefig('gdp comparison.png')


#agricultural and industrial employment comparison
# function to extract specific columns from the DFs of all countries
# for India
indf7=IN_df[['Employment in Industry(%)', 'Employment in Agriculture(%)','Country','Year']]
    
# for China
chinadf1=CN_df[['Employment in Industry(%)', 'Employment in Agriculture(%)' , 'Country','Year']]
#for USA
usadf2=US_df[['Employment in Industry(%)', 'Employment in Agriculture(%)', 'Country','Year']]
#for great britain
gbdf3=GB_df[['Employment in Industry(%)', 'Employment in Agriculture(%)','Country','Year']]
#for canada
candf4=CA_df[['Employment in Industry(%)', 'Employment in Agriculture(%)','Country','Year']]
#for south africa
southdf5=ZA_df[['Employment in Industry(%)', 'Employment in Agriculture(%)','Country','Year']]
#for Japan
japdf6=JP_df[['Employment in Industry(%)', 'Employment in Agriculture(%)','Country','Year']]
# combine the two dataframes
lst=[indf7,chinadf1,usadf2,gbdf3,candf4,southdf5,japdf6]
df6ae = pd.concat(lst)
df6ae = pd.DataFrame(df6ae)
df6ae = df6ae.reset_index(drop=True)
df6ae = df6ae[df6ae.Year == 2012]
df6ae.head(80)

# bar plot
plt.figure(figsize=(7, 5))
# plot the chart using matplotlib.pyplot library
df6ae.plot(kind='bar',x='Country',y=['Employment in Industry(%)','Employment in Agriculture(%)'],color=['purple', 'pink'])
plt.title('employment in Industries v/s Agriculture in 2012' )
plt.savefig('empolyment comparison.png')
                     

