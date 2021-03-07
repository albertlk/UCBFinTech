import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path
from datetime import datetime, timedelta
import quandl
import os
import requests
#%matplotlib inline
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

#Import SKLearn Library and Classes
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

load_dotenv()

#Retrieve currency basket weighting from countryweight.py and create currency basket
def get_basket():
    # run fundamental weighting, run main and assign to dataframe, import rename_dict to use for Quandl calls
    import countryweight 
    weights_df = countryweight.main()
    from countryweight import rename_dict


    # format countryweight symbols for Quandl calls
    weight = weights_df.copy()
    rename_sorted = {k: v for k, v in sorted(rename_dict.items(), key=lambda item:item[1])}
    index = list(rename_sorted.keys())
    weight = weight.rename(index = {'CAN':'CAD', 'THA':'THB'}).sort_index()
    weight.index = index
    transpose = weight.transpose()

    #fetch Quandl key
    quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")

    # list of currencies
    currencies = list(transpose.columns)

    # currency dataframe fetched from Quandl
    mydata = quandl.get(currencies)

    # create alternative currency basket
    #create crypto basket
    crypto = quandl.get('BCHAIN/MKPRU')
    crypto = crypto.rename(columns = {'Value':'BTC'})
    crypto = crypto.dropna()
    crypto = crypto.fillna(0)

    #create gold df and collect only US AM column
    gold = quandl.get('LBMA/GOLD')
    gold = gold.iloc[:,:1]
    gold = gold.dropna()

    #create alternate currency basket
    alt_basket = gold.join(crypto, how = 'outer')
    alt_basket = alt_basket.rename(columns = {'USD (AM)': 'GOLD'})
    alt_basket = alt_basket.replace(to_replace = np.NaN, method = 'ffill')
    alt_basket = alt_basket.fillna(0)

    #create currency_df to join all currencies
    currency_df = pd.DataFrame()

    #join alt_basket and currency_df
    currency_df = mydata.rename(columns= lambda x:x[:12])
    currency_df = currency_df.join(alt_basket, how ='inner')
    currency_df = currency_df.replace(to_replace = np.NaN, method = 'ffill')
    currency_df = currency_df.replace(to_replace = np.inf, method = 'ffill')
    currency_df = currency_df.replace(to_replace = -np.inf, method = 'ffill')
    currency_df = currency_df.fillna(0)
    
    return currency_df

#Create features
def basket_features(currency_df):
    #Calculate feature measures for trend (EWM ROC), volatility (bollinger band standard deviation ROC), and daily percent returns
    ema_window = 20 
    bolling_window = 20

    for currency in currency_df.columns:
        currency_df[f'{currency} ewm_ROC'] = currency_df[currency].ewm(halflife = ema_window).mean().pct_change()
        currency_df[f'{currency} bbVol'] = ((currency_df[currency].rolling(window=bolling_window).mean()+ currency_df[currency].rolling(window=bolling_window).std() * 1) - (currency_df[currency].rolling(window=bolling_window).mean()- currency_df[currency].rolling(window=bolling_window).std() * 1)).pct_change()    
        currency_df[f'{currency} daily return'] = currency_df[currency].pct_change()

    #apply basket weighting to currency_df daily returns
    pair = len(currency_df.columns[1])

    for currency in transpose:
        for col in currency_df.loc[:,currency_df.columns.str.endswith("daily return")]:
            if currency == col[:pair]:
                currency_df[col] = float(transpose[currency]) * currency_df[col]


    currency_df = currency_df.replace(to_replace = np.NaN, method = 'ffill')
    currency_df = currency_df.replace(to_replace = np.inf, method = 'ffill')
    currency_df = currency_df.replace(to_replace = -np.inf, method = 'ffill')
    currency_df = currency_df.replace(to_replace = 0, method = 'ffill')
    currency_df = currency_df.fillna(0)
    return currency_df

def filter_basket(currency_df):
    #drop any currency with annualized vol > 1
    drop_list = currency_df.loc[:, currency_df.columns.str.endswith('daily return')].std()*np.sqrt(252)< 1
    drop_list = drop_list[drop_list == False].rename(lambda x:x[:-13]).index
    for currency in drop_list:
        currency_df = currency_df.loc[:, ~currency_df.columns.str.startswith(currency)]

    #filter out any hyperinflationary currency where annualized vol is above .5SD
    annualized_vol = currency_df.loc[:, currency_df.columns.str.endswith('daily return')].std()*np.sqrt(252)
    drop_list = currency_df.loc[:, currency_df.columns.str.endswith('daily return')].std()*np.sqrt(252)< annualized_vol.mean()
    drop_list = drop_list[drop_list == False].rename(lambda x:x[:-13]).index

    #remove the drop_list currencies from basket
    for currency in drop_list:
        currency_df = currency_df.loc[:, ~currency_df.columns.str.startswith(currency)]

    #save df if manual inspection necessary
    #currency_df.to_pickle(r'D:\FINTECH\stable_coin_portfolio_reweight_algo\currency_features.pickle')

    return currency_df
    
#create benchmark basket, select individual currencies or for standardization, use benchmark basket already created

benchmark_list = ['FRED/DEXUSEU', 'FRED/DEXCAUS', 'ECB/EURCHF']
benchmark_data = quandl.get(benchmark_list)
benchmark_df = benchmark_data.rename(columns= lambda x:x[:12])
benchmark_df = benchmark_df.rename(columns = {'ECB/EURCHF -': 'ECB/EURCHF'})
benchmark_df = benchmark_df.dropna()

#save df if manual inspection necessary
#benchmark_df.to_pickle(r'D:\FINTECH\stable_coin_portfolio_reweight_algo\benchmark_df.pickle')

#create method annualized volatility for countryweight algo
def annualized_volatility():
    annualized_vol = mydata.rename(columns = lambda x:x[:12])
    annualized_vol = annualized_vol.pct_change()
    annualized_vol.index = annualized_vol.index.year
    annualized_vol = annualized_vol.groupby(annualized_vol.index).std()*np.sqrt(252)
    #save df if manual inspection necessary
    #annualized_vol.to_csv(r'D:\FINTECH\stable_coin_portfolio_reweight_algo\annualized_volatility.csv')
    return annualized_vol

#Random Forest model

def random_forest(currency_df):
    #create portfolio return column
    currency_df['portfolio return'] = currency_df.loc[:, currency_df.columns.str.endswith('daily return')].sum(axis=1)

    # define long/short portfolio target by calculating mean and SD, then selecting the .5 SD as the target
    portfolio_mean = currency_df['portfolio return'].std()
    portfolio_std = currency_df['portfolio return'].mean()
    portfolio_short_target = portfolio_mean + portfolio_std/4
    portfolio_long_target = portfolio_mean - portfolio_std/4

    #create trading signals df
    trading_signals_df = pd.DataFrame()


    #add dependent variable for targeting an absolute value return of 1%, shift forward looking window by user defined amount (1 day)

    count = currency_df.columns.str.contains("ewm_ROC|daily return|bbVol").sum()+1
    currency_names = currency_df.iloc[:, : -count].columns.values.tolist()

    #create feature signals- if ewm_ROC or bb VOL >< std deviation, create signal to bring back into mean reversion
    for currency in currency_names:
        trading_signals_df[f'{currency} sell signal'] = np.where((currency_df[f'{currency} ewm_ROC'] > currency_df[f'{currency} ewm_ROC'].std() *.5) | (currency_df[f'{currency} bbVol'] > currency_df[f'{currency} bbVol'].std() *.5), -1, 0)
        trading_signals_df[f'{currency} buy signal'] = np.where((currency_df[f'{currency} ewm_ROC'] > currency_df[f'{currency} ewm_ROC'].std() * -.5) | (currency_df[f'{currency} bbVol'] < currency_df[f'{currency} bbVol'].std() * -.5), 1, 0)


    #create temp_df for storing portfolio targets long and short
    temp_df = pd.DataFrame()

    temp_df['portfolio short target'] = np.where((currency_df['portfolio return'] >= portfolio_long_target), -1, 0)
    temp_df['portfolio long target'] = np.where((currency_df['portfolio return'] <= portfolio_short_target), 1, 0)

    trading_signals_df['portfolio target'] = temp_df['portfolio short target'] + temp_df['portfolio long target']

    #format df as necessary
    trading_signals_df = trading_signals_df.set_index(pd.to_datetime(currency_df.index, infer_datetime_format =True))

    # Manually splitting the data 70/30 split
    split = int(0.70 * len(trading_signals_df))

    X_train = trading_signals_df.iloc[: split, :-1]
    X_test = trading_signals_df.iloc[split:, :-1]

    y_train = trading_signals_df['portfolio target'][:split]
    y_test = trading_signals_df['portfolio target'][split:]

    #Train Random Forest Model
    # Fit a SKLearn linear regression using just the training set (X_train, Y_train):
    model = RandomForestClassifier(n_estimators=200, random_state=0)
    model.fit(X_train, y_train)

    # Make a prediction of "y" values from the X_test dataset
    predictions = model.predict(X_test)

    # Assemble actual y data (Y_test) with predicted y data (from just above) into two columns in a dataframe
    # Create synthetic Portfolio Adjusted Close column 
    Results = y_test.to_frame()
    Results["RF Predicted Value"] = predictions
    Results['Portfolio Forward Daily Returns'] = currency_df['portfolio return'].shift(-1)
    Results['Portfolio Adjusted Close'] = ((Results['Portfolio Forward Daily Returns'] * currency_df['portfolio return'].shift(-1)) + Results['Portfolio Forward Daily Returns']).shift(1)*10 + 1

    #save df if manual inspection necessary
    #RF_portfolio_results = Results.to_pickle(r'D:\FINTECH\stable_coin_portfolio_reweight_algo\RF_portfolio_results.pickle')
    return Results
    
# check results if necessary
def check_results():
    print(Results[(Results<0) | (Results > 0)].count())
    
#return last Portfolio Adjusted Close for oracle calls
def return_close_price():
    return Results['Portfolio Adjusted Close'][-1]


def main():
    #runs above code and returns Portfolio Adjust Close price
    
    currency_df = get_basket()
    currency_df = currency_features(currency_df)
    currency_df = filter_basket(currency_df)
    Results = random_forest(currency_df)
    
    return return_close_price()

