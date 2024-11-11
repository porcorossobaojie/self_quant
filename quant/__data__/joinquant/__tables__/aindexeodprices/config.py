# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 09:34:24 2021

@author: Porco Rosso
"""

class main():
    params = {'table': 'aindexeodprices', 
              'security': ['000852.XSHG', '000905.XSHG', '399300.XSHE', '000016.XSHG'],
              'fields': ['avg', 'close', 'high', 'low', 'money', 'open', 'pre_close', 'volume'],
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'S_DQ_AVGPRICE': ['double(20,4)', '均价(VWAP)'],
                          'S_DQ_CLOSE': ['double(20,4)', '收盘价'],
                          'S_DQ_HIGH': ['double(20,4)', '最高价'],
                          'S_DQ_LOW': ['double(20,4)', '最低价'],
                          'S_DQ_AMOUNT': ['double(20,6)', '成交金额(千元)'],
                          'S_DQ_OPEN': ['double(20,4)', '开盘价'],
                          'S_DQ_PRECLOSE': ['double(20,4)', '昨收盘价'],
                          'S_DQ_VOLUME': ['double(20,6)', '成交量(手)'],
                          'S_DQ_PCTCHANGE': ['double(12,8)', '涨跌幅(%%)']}, 
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE']}



