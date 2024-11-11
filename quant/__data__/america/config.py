# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 08:56:42 2023

@author: Porco Rosso
"""
token = 'd7ade34c386bde324f40b234fba3ef91'
quote_url = 'https://47.252.51.154:8443/v2/usa/stock/daily_price'
index_url = 'https://47.252.51.154:8443/v2/usa/index/daily_price'
        
import pandas as pd
    
class main():
    quote_url = 'https://47.252.51.154:8443/v2/usa/stock/daily_price'
    token_infomation = {'token':'d7ade34c386bde324f40b234fba3ef91', 
                        'fields': 'trade_date,symbol,open,close,low,high,volume,adj_open,adj_close,adj_low,adj_high,adj_volume,market_cap',
                        # 返回条数 每日行情数有几千行这里直接指定最大
                        'size': 10000, # default 100
                        # 排序
                        'symbol__order': 1,
                        'trade_date__eq':None,
                        }
    params = {'schemas': 'join_data',
              'table': 'ushareeodprices', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'S_DQ_OPEN': ['double(16, 4)', '开盘价(元)'], 
                          'S_DQ_CLOSE': ['double(16, 4)', '收盘价(元)'], 
                          'S_DQ_LOW':['double(16, 4)', '最低价(元)'], 
                          'S_DQ_HIGH': ['double(16, 4)', '最高价(元)'], 
                          'S_DQ_VOLUME': ['bigint', '成交量(股)'], 
                          'S_DQ_ADJOPEN': ['double(20, 4)', '后复权开盘价(元)'], 
                          'S_DQ_ADJCLOSE': ['double(20, 4)', '后复权收盘价(元)'], 
                          'S_DQ_ADJLOW':['double(20, 4)', '最低价(元)'], 
                          'S_DQ_ADJHIGH': ['double(20, 4)', '最高价(元)'], 
                          'S_DQ_ADJVOLUME': ['bigint', '成交量(股)'], 
                          'S_DQ_CAP': ['double(32, 2)', '市值'], 
                          'S_DQ_ADJAVGPRICE': ['double(20, 4)', '后复权VWAP(元)'], 
                          'S_DQ_AMOUNT': ['double(20, 4)', '成交额'],
                          'S_DQ_TURNOVER':['double(16, 6)', '换手率']},
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2005-01-01', '2030-12-31', freq='Y').to_list()}
              }









