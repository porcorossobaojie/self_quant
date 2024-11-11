# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:13:26 2024

@author: admin
"""



import pandas as pd
import requests


import yfinance as yf

ee = yf.Ticker('88E.AUS')

http = 'https://tsanghi.com/api/fin/stock/XASX/list?token=29614d859bd14b7681afcc591090e7b0'

df = requests.get(http)
g1 = pd.DataFrame(df.json()['data'])

data = yf.download(g2, start='2024-01-01', end='2024-02-01')
