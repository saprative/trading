# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 00:01:56 2021

@author: Saprative Jana
"""

#Import
from brokers.angleone import AngleOne
import pandas as pd
from finta import TA
import mplfinance as mpf
import talib


angle_one = AngleOne()
angle_one.historical_data("3045","ONE_DAY","2022-01-01 09:00","2022-03-01 09:16")
data_ohcl = angle_one.data_ohcl()

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