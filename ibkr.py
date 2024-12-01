from ib_insync import *

import random
import time
import datetime

import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import hurst
import yfinance
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from scipy import stats
from numpy import mean, absolute
from pandas_datareader import data as pdr
import time
from tqdm import tqdm

from backtesting import Backtest, Strategy
from backtesting.lib import crossover


import os
# Path for 'data' folder
# Create a data folder that is in the upper level directory
# e.g. 'C:\Users\user\QF621\data'

folder_path = 'data/commods_futures/'
# Check if the folder doesn't already exist
if not os.path.exists(folder_path):
    # Create the 'data' folder
    os.makedirs(folder_path)
    print("Folder 'data' created successfully.")
else:
    print("Folder 'data' already exists.")

ib = IB()
ib.connect('127.0.0.1', 7496, clientId = 1) 

DATA_FOLDER = 'data/commods_futures/'


# contract = Forex('EURUSD')
# contract.symbol = 'EUR'
# contract.secType = 'CASH'
# contract.exchange = 'IDEALPRO'

# interval = '30 mins'
# year = 1
# end_date_time = (datetime.datetime.today() - datetime.timedelta(days=365 * year)).strftime("%Y%m%d %H:%M:%S")
# frame = util.df(ib.reqHistoricalData(contract, endDateTime=end_date_time, durationStr='13 W', barSizeSetting=interval, whatToShow='Trades', useRTH=False))
# print(frame)

commods_futures = ['CL', 'GC', 'NG', 'SI', 'HG', 'PL', 'PA', 'HO', 'RB', 'BZ', 'ZC', 'KE', 'ZL', 'ZS', 'HE', 'LE', 'CC', 'KC', 'CT', 'OJ', 'SB']
commods_nymex = ['CL', 'NG', 'PL', 'PA', 'HO', 'RB', 'BZ'] # Oil, Nat Gas, Platinum, Palladium, Heating Oil, RBOB Gasoline, 
commods_comex = ['GC', 'SI', 'HG']
commods_cbot = ['ZW', 'ZC', 'ZL', 'ZS', 'ZO'] 
commods_nybot = ['CC', 'KC', 'CT', 'SB']
# ContFuture(ticker, 'NYMEX', 'USD')
# Stock(ticker, 'SMART', 'USD')
# commods_etf = ['PDBC', 'FTGC', 'DBC', 'GSG', 'BCI', 'COMT', 'DJP', 'USOI', 'KRBN', 'COM', 'CMDT', 'NBCM', 'KCCA', 'CMDY', 'BCD', 'USCI', 'HGER', 'GCC', 'FAAR', 
#               'COMB', 'FGDL', 'BDRY', 'CCRV', 'DJCB', 'BCIM', 'UCIB', 'GRN', 'DCMT', 'PIT', 'RENW', 'SDCI', 'KEUA', 'HCOM', 'EVMT', 'ZSB']

commods_etf = ['GLD', 'SLV', 'UNG', 'USO', 'IAU', 'DBC', 'DBA', 'CORN', 'DBB', 'GSG', 'DBO', 'DBE', 'USCI', 'PALL', 'SIVR', 'PPLT', 'URA', 'BNO', 'SGOL', 'UGA']

# USD_pairs = ['EURUSD', 'AUDUSD', 'USDJPY', 'GBPUSD', 'USDCAD', 'USDCHF', 'USDCNH', 'USDDKK', 'USDILS', 'KRWUSD','USDMXN', 'USDNOK', 'USDPLN', 'USDRON', 'USDSEK']
years = 5

for ticker in commods_:
    barsList = []
    contract = ContFuture(ticker, 'NYMEX', 'USD')
    for year in tqdm(range(years), desc=ticker, unit="year", leave=True):
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=(datetime.datetime.today()- datetime.timedelta(days = 365 * year)).strftime("%Y%m%d %H:%M:%S"),
            durationStr='1 Y',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=False,
            formatDate=2,
            timeout=120)
        if not bars:
            break
        dt = bars[0].date
        print(dt)
        barsList.append(bars)

        # save to CSV file
        allBars = [b for bars in reversed(barsList) for b in bars]
        df = util.df(allBars)
        df.to_csv(DATA_FOLDER + ticker  + '_daily.csv', index=False)

    

# def get_ibkr_data(ib, contract, years, interval):
#     print('Downloading symbol = {0} years = {1} interval = {2}'.format(contract.symbol, years, interval))
#     ib.qualifyContracts(contract)
#     partitions = []
#     for year in reversed(range(years)):
#         end_date_time = (datetime.datetime.today() - datetime.timedelta(days=365 * year)).strftime("%Y%m%d %H:%M:%S")
#         print('Downloading for end_date_time = {0}'.format(end_date_time))
#         partition = util.df(ib.reqHistoricalData(contract, endDateTime=end_date_time, durationStr='1 Y', barSizeSetting=interval, whatToShow='Trades', useRTH=False))
#         partition.index = partition['date']
#         partitions.append(partition)
#     frame = pd.concat(partitions)
#     frame = frame[~frame.index.duplicated(keep='first')]
#     return frame

# get_ibkr_data(ib, contract, years = 2, interval = '1 day')


'''
#################################################################################################
THIS WILL NOT WORK WITH REAL TIME TRADED SYMBOLS. IMPORT THESE SYMBOLS TO A NEW OFFLINE DATABASE.
IF YOU HAVE ISSUES, REPLY TO THIS FORUM THREAD AND I WILL HELP. DO NOT BUG TOMASZ.
#################################################################################################

things you will need: python3, TWS logged in and running.
pip packages you will need: ib_insync, pandas

About: This script downloads 1 second data as far back as you need.

Usage: Fill out the information in the two variables below. You can get this information from TWS.
       TWS>Enter Symbol>Click Futures>Click "More & Multiple">Click "Show Historical Contracts"

This version of the script now has a dialog before you run it. There are two modes. One for download X days from now
The other downloads X days from specified date. 

The script also now saves a CSV every 5 calls to the TWS API. This is basically a fail-safe. The last file will have the most data. 
All other files can be deleted once the script is finished.

'''

# ##########################################################
# # CHANGE THESE VALUES FOR THE CONTRACT YOU WANT 
# ##########################################################

# downloadFolder = 'C:\\Users\\darre\\Desktop\\macro-project\\data\\ES\\' 
# contract = 'ES' # CME FUTURES ONLY
# contractCode = 'H4'
# contractExp = '202403'

# ##########################################################
# ## Don't edit below unless you know what you're doing.
# ##########################################################


# mode = int(input("Mode: From now (1), From Date (2) -> "))
# if mode == 1:
#     daysBack = int(input("Number of Days back from now to download -> ")) # Number of days to download. Sart day/ time is the moment you run this script.
#     contracts = [[contract,contract+contractCode,contractExp,datetime.datetime.today(),(datetime.datetime.today() - datetime.timedelta(days=daysBack))]]
# else:
#     dateAndTime = str(input("Date Time EX: 03/18/2021 22:48:28 -> "))
#     daysBack = int(input("Number of days back from date to download -> "))
#     contracts = [[contract,contract+contractCode,contractExp,datetime.datetime.strptime(dateAndTime, '%m/%d/%Y %H:%M:%S'),(datetime.datetime.strptime(dateAndTime, '%m/%d/%Y %H:%M:%S') - datetime.timedelta(days=daysBack))]]

# ##### Don't edit below unless you know what you're doing ;^)  ######

# def csvOut(barsList, n, fileName):
#     allBars = [b for bars in reversed(barsList) for b in bars]
#     df = util.df(allBars)
#     gfg_csv_data = df.to_csv(downloadFolder+str(n)+'-'+fileName+'.csv', index = True)
#     #df.drop(df.index,inplace=True) # clear the dataframe
#     print('Exported: '+str(n)+'-'+fileName+'.csv')


# def getData(contracts):
#     i = 0
#     n = 0
#     for contract in contracts:
#         symbol = contract[0]
#         fileName = contract[1]
#         contractMonth = contract[2]
#         end = contract[3]
#         start = contract[4]

#         print('Contract: '+ fileName + ' ' + contractMonth)
#         print('Downloading...')

#         barsList = []

#         contract = Contract(secType='FUT',symbol=symbol, lastTradeDateOrContractMonth=contractMonth, exchange='CME', currency='USD', includeExpired=True)

#         dt = end
#         running = True
#         while dt > start and running:
#             if dt.weekday() == 5:
#                 # if it's saturday, go back to friday, eod.
#                 dt = dt - datetime.timedelta(days=1)
#                 dt = dt.replace(hour=13, minute=59, second=0)
#             else:
#                 bars = ib.reqHistoricalData(contract, endDateTime=dt, durationStr='13 W', barSizeSetting='30 mins', whatToShow='TRADES', useRTH=False) #,timeout=0
#                 barsList.append(bars)
                
#                 dt = bars[0].date
#                 print(fileName + ' ' + dt.strftime('%m/%d/%Y %H:%M:%S') + ' Done.')
#                 if(i == 4):
#                     csvOut(barsList,n,fileName) #export dataframe
                   
#                     i = 0
#                     n+=1
#                 else:
#                     i+=1
#                 time.sleep(10.2)
#         if running:
#              csvOut(barsList,n,fileName)
            

#         print('Done.')
#     print('All contracts downloaded. :^)')

# getData(contracts)
