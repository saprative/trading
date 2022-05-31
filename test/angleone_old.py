# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 00:01:56 2021

@author: Saprative Jana
"""

#Import

import pandas as pd
from finta import TA
import mplfinance as mpf
import talib
import xlwings as xw


import pandas as pd


# package import statement for API
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)

# Detail
CLIENT_ID = "S1118627"
PASSWORD = "Root2eq1.414"

class AngleOne():
    
    def __init__(self):
        #create object of call
        self.obj=SmartConnect(api_key="4Dci0TUJ")
                        #optional
                        #access_token = "your access token",
                        #refresh_token = "your refresh_token")

        #login api call
        data = self.obj.generateSession(CLIENT_ID,PASSWORD)
        refreshToken= data['data']['refreshToken']

        #fetch the feedtoken
        feedToken=self.obj.getfeedToken()

        #fetch User Profile
        userProfile= self.obj.getProfile(refreshToken)
        
    def historical_data(self,symbol,interval,fromdate,todate):
        #Historic api
        try:
            historicParam={
            "exchange": "NSE",
            "symboltoken": symbol,
            "interval": interval,
            "fromdate": fromdate, 
            "todate": todate
            }
            self.data = self.obj.getCandleData(historicParam)
            self.data_ohcl = pd.DataFrame(self.data['data'])
            self.data_ohcl.columns = ['Date','Open','High','Low','Close','Volume']
            print(self.data_ohcl)
            return self.data_ohcl
        except Exception as e:
            print("Historic Api failed: {}".format(e.message))
        
    
    def logout(self):
        #logout
        try:
            logout=self.obj.terminateSession(CLIENT_ID)
            print("Logout Successfull")
        except Exception as e:
            print("Logout failed: {}".format(e.message))
        



#Historic api
# try:
#     historicParam={
#     "exchange": "NSE",
#     "symboltoken": "3045",
#     "interval": "ONE_DAY",
#     "fromdate": "2022-01-01 09:00", 
#     "todate": "2022-03-01 09:16"
#     }
#     data = obj.getCandleData(historicParam)

# except Exception as e:
#     print("Historic Api failed: {}".format(e.message))

# Data Anlysis

# data_ohcl['Date'] = pd.to_datetime(data_ohcl['Date'])

# data_ohcl.shape
# data_ohcl.head(3)
# data_ohcl.tail(3)
# data_ohcl['Date'] = data_ohcl['Date'].dt.tz_convert(None)
# print(data_ohcl.info())


# print(data_ohcl)


angle_one = AngleOne()
data_ohcl = angle_one.historical_data("3045","ONE_DAY","2022-01-01 09:00","2022-03-01 09:16")

# mpf plot
data_mpf = data_ohcl
data_mpf.index = pd.DatetimeIndex(data_ohcl['Date'])
mpf.plot(
    data_mpf,
    type='candle',
    title='Apple, March - 2020',
    ylabel='Price (Rs)',
    mav=(5,18),
    volume=True)
angle_one.logout()