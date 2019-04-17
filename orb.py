# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:39:40 2019

@author: The Imperium
"""

import requests
import json
import pandas as pd
profit_nett = 0
loss_nett = 0
total_trades = 0
total_loss_trades = 0
#Fetch FNO Stocks
fnoStocks = []
url= 'https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/foSecStockWatch.json'
r = requests.get(url)
data = r.json()
fnoStocks = []
stockList = data['data']
for symbol in stockList:
    fno = (symbol['symbol'])
    fnoStocks.append(fno)
fnoStocks.sort()
for stock in fnoStocks:
    instrumentList = pd.read_csv("instruments.csv")
    dataToken = instrumentList[instrumentList['tradingsymbol']==stock]
    dataToken = dataToken[dataToken['exchange']=='NSE']
    instrument_token = dataToken.instrument_token.iloc[0]
    r = requests.get('#urlfordata')
    data = r.content
    data = json.loads(data)
    data = data['data']['candles']
    profit_total = 0
    loss_total = 0
    trade = 0
    loss_trade = 0
    for day in range(0,len(data)-1):
        
        if data[day+1][1] > data[day][2]:
           tdate = data[day+1][0].split('T')[0] 
           fivemd = requests.get('#Urlfordata')
           fivemd = fivemd.content
           fivemd = json.loads(fivemd)
           fivemd = fivemd['data']['candles']
           fivemd_new = fivemd[1:]
           df = pd.DataFrame.from_records(fivemd_new, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
           try:
               if fivemd[1][2] > fivemd[0][2] : 
                   trade += 1
                   long_price = fivemd[0][2] + 0.05
                   stop_loss = fivemd[0][3] - 0.05
                   if ((df['Open'] <= stop_loss) & (df['High'] <= stop_loss)& (df['Low'] <= stop_loss)& (df['Close'] <= stop_loss)).any() == True:
                       loss = long_price - stop_loss
                       loss_trade +=1
                       loss_total += loss
                   else:
                       profit = float(df.values[-1][4]) - long_price
                       profit_total += profit
               elif fivemd[1][3] < fivemd[0][3] : 
                   trade += 1
                   short_price = fivemd[0][3]-0.05
                   stop_loss = fivemd[0][2]+0.05
                   if ((df['Open'] >= stop_loss) & (df['High'] >= stop_loss)& (df['Low'] >= stop_loss)& (df['Close'] >= stop_loss)).any() == True:
                       loss = stop_loss - short_price 
                       loss_trade += 1
                       loss_total += loss
                   else:
                       profit = short_price -float(df.values[-1][4]) 
                       profit_total += profit
           except:
                pass
        
    print("Total trades triggered in "+stock+": "+str(trade))           
    print("Win rate in "+stock+": "+str(((trade-loss_trade)/trade)*100))
    print("Net P/L in "+stock+": "+str(profit_total-loss_total))
    with open('result.txt','a') as file:
        file.write("Total trades triggered in "+stock+": "+str(trade)+"\n")
        file.write("Win rate in "+stock+": "+str(((trade-loss_trade)/trade)*100)+"\n")
        file.write("Net P/L in "+stock+": "+str(profit_total-loss_total)+"\n")
        file.write("=============================================================================================")
    total_trades += trade
    total_loss_trades += loss_trade
    profit_nett += profit_total
    loss_nett += loss_total
print("Total trades triggered in ORB "+": "+str(total_trades)+"\n")           
print("Win rate in ORB"+": "+str(((total_trades-total_loss_trades)/total_trades)*100)+"\n")
print("Net P/L in ORB"+": "+str(profit_nett-loss_nett)+"\n")
with open('result.txt','a') as file:
        file.write("Total trades triggered in ORB "+": "+str(total_trades)+"\n")
        file.write("Win rate in ORB"+": "+str(((total_trades-total_loss_trades)/total_trades)*100)+"\n")
        file.write("Net P/L in ORB"+": "+str(profit_nett-loss_nett)+"\n")