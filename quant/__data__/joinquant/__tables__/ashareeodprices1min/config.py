# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:17 2021

@author: Porco Rosso
"""
import pandas as pd

class main():
    params = {'table': 'ashareeodprices1min', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(10)', '股票代码'],
                          'S_MQ_OPEN': ['double(8, 2)', '开盘价(元)'], 
                          'S_MQ_CLOSE': ['double(8, 2)', '收盘价(元)'], 
                          'S_MQ_LOW':['double(8, 2)', '最低价(元)'], 
                          'S_MQ_HIGH': ['double(8, 2)', '最高价(元)'], 
                          'S_MQ_VOLUME': ['bigint', '成交量(股)'], 
                          'S_MQ_AMOUNT': ['bigint', '成交量(元)'], 
                          'S_MQ_LOW_LIMIT': ['double(12, 2)', '收盘价(元)'], 
                          'S_MQ_HIGH_LIMIT': ['double(14, 2)', '收盘价(元)'], 
                          'S_MQ_PCTCHANGE': ['double(10, 6)', '涨跌幅'],
                          },
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT'], 
              'partition': {'TRADE_DT': pd.date_range('2017-01-01', '2030-12-31', freq='M').to_list()}
              }
              

