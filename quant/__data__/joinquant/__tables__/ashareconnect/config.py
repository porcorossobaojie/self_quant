# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:17 2021

@author: Porco Rosso
"""
import pandas as pd

class main():
    params = {'table': 'ashareconnect', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'S_DQ_LINKID': ['int(8)', '市场通编码\n310001-沪股通,310002-深股通,310005-港股通'], 
                          'S_DQ_SCOUNT': ['BIGINT(36)', '单位: 股,于中央结算系统的持股量'], 
                          'S_DQ_SRATIO':['double(8, 6)', '沪股通: 占于上交所上市及交易的A股总数的百分比\n深股通:占于深交所上市及交易的A股总数的百分比;\n港股通:占已发行股份百分比'], },
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2017-01-01', '2030-12-31', freq='Y').to_list()}
              }
              

