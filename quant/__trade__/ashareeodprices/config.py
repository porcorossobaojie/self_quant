# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:17 2021

@author: Porco Rosso
"""
import pandas as pd

class main():
    params = {'table': 'ashareeodprices', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'S_DQ_OPEN': ['double(12, 2)', '开盘价(元)'], 
                          'S_DQ_CLOSE': ['double(12, 2)', '收盘价(元)'], 
                          'S_DQ_LOW':['double(12, 2)', '最低价(元)'], 
                          'S_DQ_HIGH': ['double(12, 2)', '最高价(元)'], 
                          'S_DQ_VOLUME': ['bigint', '成交量(股)'], 
                          'S_DQ_AMOUNT': ['bigint', '成交量(元)'], 
                          'S_DQ_HIGH_LIMIT': ['double(12, 2)', '涨停价(元)'], 
                          'S_DQ_LOW_LIMIT': ['double(12, 2)', '跌停价(元)'], 
                          'S_DQ_AVGPRICE': ['double(12, 2)', 'VWAP(元)'], 
                          'S_DQ_PRECLOSE': ['double(12, 2)', '昨收盘价(元)'], 
                          'S_DQ_TRADESTATUS': ['int(1)', '交易状态'], 
                          'S_DQ_POST_FACTOR': ['double(16, 6)', '后复权因子'], 
                          'S_DQ_ADJOPEN': ['double(18, 8)', '后复权开盘价(元)'], 
                          'S_DQ_ADJCLOSE': ['double(18, 8)', '后复权收盘价(元)'], 
                          'S_DQ_ADJAVGPRICE': ['double(18, 8)', '后复权VWAP(元)'], 
                          'S_DQ_ADJPRECLOSE': ['double(18, 8)', '后复权昨收盘价(元)'], 
                          'S_DQ_PCTCHANGE': ['double(10, 8)', '涨跌幅']},
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2005-01-01', '2030-12-31', freq='Y').to_list()}
              }
              

