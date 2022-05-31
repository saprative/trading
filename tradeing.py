# -*- coding: utf-8 -*-
"""
Created on Tue May 31 13:46:30 2022

@author: Saprative Jana
"""

import pandas as pd
import ta
import xlwings as xw
import re

#internal 
import angleone

# -----------------Excel------------------------------

def watchlist_manager():
    global watchlist, indicators, watch_sheet
    
    print(" -------------- Algo Starting ---------------------")
    wb = xw.Book('trading.xlsx')
    watch_sheet = wb.sheets[0]
    watchlist = watch_sheet.range('A2').expand().value
    indicators = watch_sheet.range('C1').expand("right").value
    print("Watchlist: {}".format(watchlist))
    print("Indictors: {}".format(indicators))
    
    
watchlist_manager()

def push_indicator():
    
    indicator_current_value_total = []
    
    
    for symbol in watchlist:
        data = angleone.historical_data(symbol,"ONE_MINUTE")
        
 
        indicator_current_value = []
        for a,i in enumerate(indicators):
            indicator_array = re.split('[()]',i)
            indicator = indicator_array[0]
            timeframe = int(indicator_array[1])
            
            if indicator=="RSI":
                data['RSI'+'('+str(timeframe)+')'] = ta.momentum.RSIIndicator( data['Close'],window=timeframe, fillna = True).rsi()
                indicator_current_value.append(round(data.loc[data.shape[0] - 1]['RSI'+'('+str(timeframe)+')'],2))
            if indicator=="EMA":
                data['EMA'+'('+str(timeframe)+')'] = ta.trend.EMAIndicator(data['Close'],window=timeframe,fillna=True).ema_indicator()
                indicator_current_value.append(round(data.loc[data.shape[0] - 1]['EMA'+'('+str(timeframe)+')'],2))
        indicator_current_value_total.append(indicator_current_value)
  
    
    watch_sheet.range('C2').value = indicator_current_value_total
    (" -------------- Updated Indicators ---------------------")
       

push_indicator()


def tick_data_feed():
    
    ticklist=watchlist
    
    def on_message(ws, message):
        print("Ticks: {}".format(message))
        
        
    angleone.tick_manager(ticklist,on_message)
    
# tick_data_feed()
    
    