# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:11:12 2022

@author: Saprative Jana
"""


import xlwings as xw
import zrd_login
import pdb
import pandas as pd
import datetime
import time
import ta
import string


"""
ts = trading_sheet
si = single_indicator
"""
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd
import datetime
import pdb
from pandas.io.json import json_normalize
import ta



api_k = "aaaaaaaaaaaaaa"  # api_key
api_s = "aaaaaaaaaaaaaa"  # api_secret
access_token = "aaaaaaaaaaaaaa"

def get_login(api_k, api_s):
	print("logging into zerodha")
	global kws, kite
	kite = KiteConnect(api_key=api_k)

	# print("[*] Generate Request Token : ", kite.login_url())
	# request_tkn = input("[*] Enter Your Request Token Here : ")
	# data = kite.generate_session(request_tkn, api_secret=api_s)
	# kite.set_access_token(data["access_token"])
	# kws = KiteTicker(api_k, data["access_token"])
	# print(data['access_token'])


	kite.set_access_token(access_token)
	kws = KiteTicker(api_k, access_token)


	return kite

kite = get_login(api_k, api_s)



def data_downloader(name, timeframe):

	print("inside of data_downloader in zrd_login")
	timeframe_number_to_char = {'1':"minute",	'365':"day",	'3':"3minute",	'5':"5minute",	'10':"10minute",	'15':"15minute",	'30':"30minute",	'60':"60minute"}


	timeframe_string = timeframe_number_to_char[timeframe]
	token = kite.ltp(['NSE:'+name])['NSE:'+name]['instrument_token']

	to_date = datetime.datetime.now().date()
	from_date = to_date - datetime.timedelta(days=2)
	data = kite.historical_data(token, from_date, to_date, timeframe_string)
	df = pd.DataFrame(data)

	return df


def send_all_indicator(df):

	df['rsi'] = ta.momentum.RSIIndicator( df['close'], n = 14, fillna = True).rsi() 

	df['ma14'] = ta.trend.SMAIndicator( df['close'], n = 14, fillna = True).sma_indicator()
	df['ma28'] = ta.trend.SMAIndicator( df['close'], n = 28, fillna = True).sma_indicator()
	
	macd = ta.trend.MACD( df['close'], n_slow = 26, n_fast = 12, n_sign = 9, fillna = True)

	df['macd'] = macd.macd()
	df['macd_signal'] = macd.macd_signal() 
	i.SuperTrend(df, period = 7, multiplier = 3, ohlc=['open', 'high', 'low', 'close'])

	return df


def init():
	global ts, kite, watchlist, indicator_name, push_tick_data_cell, orderbook, margins

	wb = xw.Book('Easy_Algo.xlsx')

	ts = wb.sheets['Trading']
	orderbook = wb.sheets['orderbook']
	margins = wb.sheets['margins']


	watchlist = ts.range('A2').expand().value
	indicator_name = ts.range('U1').expand().value[0]
	push_tick_data_cell = 'F1'

	kite = zrd_login.kite

init()


def push_tick_data(watchlist, ts, c_time):

	print(f"tick updated {c_time}")

	zrd_name = ['NSE:' + x for x in watchlist]
	data = kite.quote(zrd_name)
	df = pd.DataFrame(data).T

	df.set_index = df['last_price']
	df = df[['instrument_token', 'timestamp', 'last_trade_time','last_quantity', 'buy_quantity', 'sell_quantity', 'volume','average_price', 'oi', 'oi_day_high', 'oi_day_low', 'net_change','lower_circuit_limit', 'upper_circuit_limit']]
	ts.range(push_tick_data_cell).value = df

	




def push_indicator(watchlist, 
                   indicator_name, ts):

	for si in indicator_name:



		try:			
			timeframe = si.split("_")[0]
			indi_name = si.split("_")[1].split("(")[0]
			parameter = int(si.split("_")[1].split("(")[1][:-1])
		except Exception as e:
			print(e)
			pdb.set_trace()

		print(si, timeframe, indi_name, parameter)

		for name in watchlist:
			df = zrd_login.data_downloader(name, timeframe)
			cell_no =  string.ascii_lowercase[indicator_name.index(si) + 20] + str(watchlist.index(name) + 2)



			if indi_name == "rsi":
				df['rsi'] = ta.momentum.RSIIndicator( df['close'], n = parameter, fillna = True).rsi()
				rsi_val = round(df.loc[df.shape[0] - 1]['rsi'], 1)
				ts.range(cell_no).value = rsi_val

			if indi_name == "ma":
				df['rsi'] = ta.trend.SMAIndicator( df['close'], n = parameter, fillna = True).sma_indicator()
				rsi_val = round(df.loc[df.shape[0] - 1]['rsi'], 1)
				ts.range(cell_no).value = rsi_val


def place_buy_sell(ts):

	end = len(watchlist) + 2
	for row_no in range(2, end):
		pdb.set_trace()

		buy = ts.range( 'b' + str(row_no)).value
		sell = ts.range( 'c' + str(row_no)).value
		qty = ts.range( 'd' + str(row_no)).value
		remark = ts.range( 'e' + str(row_no)).value


		if (buy == "buy") and (remark is None):
			kite.place_order(name, )
			ts.range( 'e' + str(row_no)).value = "placed_buy_order"

		if (sell == "sell") and (remark is None):
			kite.place_order(name, )
			ts.range( 'e' + str(row_no)).value = "placed_sell_order"


def send_orderbook(ts):
	ords = kite.orders()
	df = pd.DataFrame(ords)
	
	df = df[['placed_by', 'order_id', 'exchange_order_id', 'parent_order_id','status', 'status_message', 'status_message_raw', 'order_timestamp','exchange_update_timestamp', 'exchange_timestamp', 'variety','exchange', 'tradingsymbol', 'instrument_token', 'order_type','transaction_type', 'validity', 'product', 'quantity','disclosed_quantity', 'price', 'trigger_price', 'average_price','filled_quantity', 'pending_quantity', 'cancelled_quantity','market_protection','tag', 'guid']]
	orderbook.range('b2').value = df





while True:
	c_time = datetime.datetime.now().strftime("%X")

	
	push_tick_data(watchlist, ts, c_time)
	# push_indicator(watchlist, indicator_name, ts)
	# place_buy_sell(ts)
	send_orderbook(ts)