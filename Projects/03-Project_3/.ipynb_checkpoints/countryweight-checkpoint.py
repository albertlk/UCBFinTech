# For reading in API Keys
import os
from dotenv import load_dotenv

# For basic analysis
import pandas as pd
from pathlib import Path
import numpy as np
import time

# For parsing through JSON dumps from API calls
import requests
import json

# Importing libraries for regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn import linear_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from sklearn.metrics import mean_squared_error, r2_score

##### RETRIEVING ECON INDICATORS #####

# Base URL for World Bank API
wb_api_base = "http://api.worldbank.org/v2/country/"

# Dictionary of user given indicators with their Corresponding API indicators
ind_dict = {
    "GDP":"NY.GDP.MKTP.CD", # GDP
    "GDG":"NY.GDP.MKTP.KD.ZG", # GDP Growth YoY
    "GDC":"NY.GDP.PCAP.CD", # GDP per Capita
    "CPI":"FP.CPI.TOTL.ZG", # CPI
    #"CAB":"BN.CAB.XOKA.GD.ZS", # Current Account Balance as % of GDP
    "UEM":"SL.UEM.TOTL.NE.ZS" # Unemployment rate
}

# Countries included for evaluation for currency basket
full_country_basket = [
    "USA", # USA
    "AUS", # Australia
    "BRA", # Brazil
    "GBR", # Great Britain
    "CAN", # Canada
    "IND", # India
    "JPN", # Japan
    "MYS", # Malaysia
    "MEX", # Mexico
    "NZL", # New Zealand
    "NOR", # Norway
    "SGP", # Singapore
    "ZAF", # South Africa
    "KOR", # South Korea
    "LKA", # Sri Lanka
    "SWE", # Sweden
    "CHE", # Switzerland
    "THA", # Thailand
    "CHN", # China
    "EUU" # European Union
]
# Note Taiwan is not included in the World Bank's Data Set

def getEconIndicator (indicator, num, countries, training = False):
    """
    Returns the indicators for the given list of countries as reported by the World Bank in the form of a pandas Dataframe
    
    Countries must be given as their 3-Digit ISO Code (https://countrycode.org/) and in the form of a list
    
    Indicator must be selected from the ind_dict defined above.
    """
    ind_data_dict = {}

    # Validating Indicators
    dict_keys = list(ind_dict.keys())
    if indicator not in dict_keys:
        raise Exception("This indicator is not supported.")
    
    # Setting indicator into API form
    api_ind = "/indicator/" + ind_dict[indicator] + f"?mrnev={num}&per_page=500&format=json"    
    
    # Building request URL.
    countries = ";".join(countries)
    wb_api_url = wb_api_base + countries + api_ind
    
    # Sending request to World Bank API
    api_response = requests.get(wb_api_url)
    attempts = 1
    
    # Error handling for API calls
    while (api_response.status_code != 200) & (attempts < 11):
        print("Retrying API call for: " + indicator + " in 10 seconds.")
        time.sleep(10)
        api_response = requests.get(wb_api_url)
        attempts += 1
        
    if api_response.status_code != 200:
        raise Exception("API call failed for" + indicator + "with reason code" + api_response.status_code)
    
    # Parsing out body of returned JSON
    ind_json = api_response.json()
    ind_json = ind_json[1]
    
    if training:
        # Creating dictionary of indicator by country ID
        for entry in ind_json:
            ind_data_dict[entry["countryiso3code"] + entry["date"]] = [entry["date"], entry["value"]]
            
        # Converting dictionary to pandas Dataframe    
        ind_data_df = pd.DataFrame.from_dict(ind_data_dict, orient = "index", columns = [indicator + " Year", indicator])
    else:
        # Creating dictionary of indicator by country ID
        for entry in ind_json:
            ind_data_dict[entry["countryiso3code"]] = [entry["value"]]
        
        # Converting dictionary to pandas Dataframe    
        ind_data_df = pd.DataFrame.from_dict(ind_data_dict, orient = "index", columns = [indicator])
    
    return ind_data_df

def getAllIndicators (countries):
    """
    Returns the all of the defined indicators (in ind_dict) for the given list of countries as reported by the World Bank 
    Countries must be given as their 3-Digit ISO Code (https://countrycode.org/) and in the form of a list
    
    Data returned in the form of a pandas DataFrame
    """
    
    dict_keys = list(ind_dict.keys())
    counter = 1
    
    for ind in dict_keys:
        if counter == 1:
            all_data_df = getEconIndicator(ind, 1, countries)
            counter += 1
        else:
            temp_data_df = getEconIndicator(ind, 1, countries)
            all_data_df = pd.concat([all_data_df, temp_data_df], axis = "columns", join = "outer")
            counter += 1
            
    return all_data_df

def getAllIndicatorsTraining (num, countries):
    """
    This function is for preparing data for training. 
    
    Num is the number of values for each metric that should be pulled.
    
    Returns the all of the defined indicators (in ind_dict) for the given list of countries as reported by the World Bank 
    Countries must be given as their 3-Digit ISO Code (https://countrycode.org/) and in the form of a list
    
    Data returned in the form of a pandas DataFrame
    """
    
    dict_keys = list(ind_dict.keys())
    counter = 1
    
    for ind in dict_keys:
        if counter == 1:
            all_data_df = getEconIndicator(ind, num, countries, True)
            counter += 1
        else:
            temp_data_df = getEconIndicator(ind, num, countries, True)
            all_data_df = pd.concat([all_data_df, temp_data_df], axis = "columns", join = "inner")
            counter += 1
            
    cols = []
    for ind in ind_dict:
        cols.append(ind + " Year")

    all_data_df.drop(columns = cols[1:], inplace = True)
    all_data_df.rename(columns = {cols[0]: "Year"}, inplace = True)
    
    return all_data_df

def relativeStrength(allIndicators, training = True):
    """
    Takes in the indicators of the full country basket and assigns relative strengths based on the maximum value of each.
    """
    
    if training:
        relativeIndicators = allIndicators.sort_values("Year")
        current_year = int(relativeIndicators["Year"].min())
        max_year = int(relativeIndicators["Year"].max())

        # Looping through by year and normalizing GDP and GDP per capita by max value
        while current_year <= max_year:

            relativeIndicators.loc[relativeIndicators["Year"] == str(current_year), "Rel GDP"] = relativeIndicators["GDP"]/relativeIndicators.loc[relativeIndicators["Year"] == str(current_year)]["GDP"].max()
            relativeIndicators.loc[relativeIndicators["Year"] == str(current_year), "Rel GDC"] = relativeIndicators["GDC"]/relativeIndicators.loc[relativeIndicators["Year"] == str(current_year)]["GDC"].max()

            current_year += 1
    
    else:
        relativeIndicators = allIndicators.copy()
        relativeIndicators["Rel GDP"] = relativeIndicators["GDP"]/relativeIndicators["GDP"].max()
        relativeIndicators["Rel GDC"] = relativeIndicators["GDC"]/relativeIndicators["GDC"].max()
        
    relativeIndicators = relativeIndicators.drop(columns = ["GDP", "GDC"])
    
    return relativeIndicators

##### TRAINING MODEL FOR INDICATORS #####

# For renaming the training dataset
rename_dict = {
    'FRED/DEXUSAL':'AUS',
    'FRED/DEXBZUS':'BRA',
    'FRED/DEXUSUK':'GBR',
    'FRED/DEXCAUS':'CAD',
    'FRED/DEXCHUS':'CHN',
    'FRED/DEXUSEU':'EUU',
    'FRED/DEXINUS':'IND',
    'FRED/DEXJPUS':'JPN',
    'FRED/DEXMAUS':'MYS', 
    'FRED/DEXMXUS':'MEX',
    'FRED/DEXUSNZ':'NZL', 
    'FRED/DEXNOUS':'NOR',
    'FRED/DEXSIUS':'SGP',
    'FRED/DEXSFUS':'ZAF',
    'FRED/DEXKOUS':'KOR',
    'FRED/DEXSDUS':'SWE',
    'FRED/DEXSZUS':'CHE',
    'FRED/DEXTHUS':'THB'
}

def getFeatures():
    """
    Getting features required for training and testing ML models
    """
    # Getting Training Economic Indicators from World Bank (From EconIndicators.ipynb)
    raw_data = getAllIndicatorsTraining(20, full_country_basket)
    norm_data = relativeStrength(raw_data)
    
    # Reading in annualized volatility data for training
    avol_csv = pd.read_csv("annualized_volatility.csv", index_col = "Date")
    avol_csv = avol_csv.loc[2004:]
    avol_csv.rename(columns = rename_dict, inplace = True)
    avol_csv.drop(columns = ['FRED/DEXDNUS', 'FRED/DEXHKUS', 'FRED/DEXTAUS', 'FRED/DEXVZUS'], inplace = True)
    
    # Creating df to match the format of the df provided by EconIndicators
    avol_dict = {}
    for country in avol_csv.columns:
        for year in avol_csv[country].index:
            # Subtracting a year as the previous year's volatility will be predicting the next 
            avol_dict[country + str(year-1)] = avol_csv[country][year]

    avol_df = pd.DataFrame.from_dict(avol_dict, orient = "index", columns = ["Annual Volatility"])
    
    features = pd.concat([norm_data, avol_df], axis = "columns", join = "inner")
    
    return features

def trainEconLinearRegresion(features):
    """
    Trains a linear regression model on the given input features. Returns the fitted model, comparison df, 
    and the mse of the test cohort 
    """
    
    X = features.drop(columns = ["Year", "Annual Volatility"])
    y = features["Annual Volatility"]
    
    # Establishing test/train split for Linear Regression
    X_lin_train, X_lin_test, y_lin_train, y_lin_test = train_test_split(X, y, random_state = 1)

    # Creating and fitting model
    model_lin = linear_model.LinearRegression()
    model_lin.fit(X_lin_train, y_lin_train)

    # Predicting results and creating df for comparison
    comp_df = y_lin_test.to_frame()
    predictions_lin = model_lin.predict(X_lin_test)
    comp_df["Predicted Volatility"] = predictions_lin
    
    mse = mean_squared_error(y_lin_test, predictions_lin)
    
    return model_lin, comp_df, mse

##### CALCULATING WEIGHTS OF CURRENCIES (BY COUNTRY) BASED ON MODEL RESULTS #####

def getWeights(volatility_df, cut_off = 0.75):
    """
    Returns the weighting recommendation for the selected % most stable currencies.
    """
    # Subtracting out the volatility at the selected % mark. All values less than 0 are set to 0
    volatility_df["InvWt"] = volatility_df["Predicted Volatility"].quantile(cut_off) - volatility_df["Predicted Volatility"]
    volatility_df.loc[volatility_df["InvWt"] < 0, "InvWt"] = 0
    
    volatility_df["Basket Weight"] = volatility_df["InvWt"]/volatility_df["InvWt"].sum()
    
    weights_df = volatility_df.drop(columns = ["Predicted Volatility", "InvWt"])
    
    return weights_df

def main():
    """
    Runs the above code and returns the weights
    """
    
    features_df = getFeatures()
    model, results, mse_score = trainEconLinearRegresion(features_df)

    recent_data = getAllIndicators(full_country_basket)
    recent_data_norm = relativeStrength(recent_data, False)

    predictions_df = pd.DataFrame(
        data = model.predict(recent_data_norm), 
        index = recent_data_norm.index, 
        columns=["Predicted Volatility"])

    weights_df = getWeights(predictions_df)
    
    return weights_df