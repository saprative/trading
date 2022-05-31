# -*- coding: utf-8 -*-
"""
Created on Sun May 29 13:33:29 2022

@author: Saprative Jana
"""

import pandas as pd
import talib
import xlwings as xw
import datetime
import requests
import pdb

#AngleOne
from smartapi import SmartConnect, SmartWebSocket

#-----------------------AngleOne-------------------------------
#Client Code
def angleone_connect():
    
    global angleone, symbol_data
    
    CLIENT_ID = "S1118627"
    PASSWORD = "Root2eq1.414"
    
    #Smart Connect
    angleone=SmartConnect(api_key="4Dci0TUJ")
                    #optional
                    #acceticker_token = "your acceticker token",
                    #refresh_token = "your refresh_token")
    
    #login api call
    data = angleone.generateSession(CLIENT_ID,PASSWORD)
    refreshToken= data['data']['refreshToken']
    
    #fetch User Profile
    userProfile= angleone.getProfile(refreshToken)
    # print("Connected: {}".format(userProfile))
    print(" Angleone Loading ....")
    

    #symbol_data
    symbol_request = requests.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")
    symbol_data = pd.DataFrame(symbol_request.json())
    
angleone_connect()
      
# --------------------------------------------------------------------

# --------------------- Utils --------------------------------------------

def get_symbol_code(symbol):
    symbol_code = symbol_data.loc[symbol_data["name"]==symbol]['token'].values[0]
    return symbol_code

# ---------------------------------------------------------------------

#------------------- Historical Data --------------------------------
def historical_data(symbol,interval):
    to_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    from_date_calulate = datetime.datetime.now() - datetime.timedelta(days=2)
    from_date = from_date_calulate.strftime("%Y-%m-%d %H:%M")
    symbol_code = get_symbol_code(symbol)
    historicParam={
        "exchange": "NSE",
        "symboltoken": symbol_code,
        "interval": interval,
        "fromdate": from_date, 
        "todate": to_date
    }
    try:
        data = angleone.getCandleData(historicParam)
        data_ohcl = pd.DataFrame(data['data'])
        data_ohcl.columns = ['Date','Open','High','Low','Close','Volume']
        # print(data_ohcl)
        return data_ohcl
    except Exception as e:
        print("Historic Api failed: {}".format(e))

# ------------------------------------------------------

#
# --------- Ticker ------------------------------------------
def tick_manager(ticklist,on_message):
    feedToken=angleone.getfeedToken()
    CLIENT_ID = "S1118627"
    
    tickcodelist = [get_symbol_code(tick) for tick in ticklist]
    
    # # token="mcx_fo|224395"
    # token="nse_cm|3045"    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
    # # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
    
    # token="nse_cm|6710&nse_cm|12740&nse_cm|5097&nse_cm|6553"
    token= "" 
    
    for tickcode in tickcodelist:
        if token=="":
            token= "nse_cm|"+tickcode
        else:
            token= token+"&nse_cm|"+ tickcode           
    
    print(token)
    
   
    task="mw"   # mw|sfi|dp
    
    ticker = SmartWebSocket(feedToken, CLIENT_ID)
    
    def on_open(ws):
        print(" ----------------------- Ticker Start ---------------------------- ")
        ticker.subscribe(task,token)
        
    def on_error(ws, error):
        print("Ticker Error: ".format(error))
        
    def on_close(ws):
        print(" ----------------------- Ticker Stop ----------------------------")
    
    # Assign the callbacks.
    ticker._on_open = on_open
    ticker._on_message = on_message
    ticker._on_error = on_error
    ticker._on_close = on_close
    ticker.connect()
    
    return ticker

# -----------------------------------------------------