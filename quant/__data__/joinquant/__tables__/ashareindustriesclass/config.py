# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 10:10:12 2021

@author: Porco Rosso
"""

import pandas as pd

class main():
    params = {'table': 'ashareindustriesclass', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'S_SWL1_CODE': ['int', '申万一级分类'], 
                          'S_SWL2_CODE': ['int', '申万二级分类'], 
                          'S_SWL3_CODE':['int', '申万三级分类'], 
                          'S_JQL1_CODE': ['varchar(8)', '聚宽一级分类'], 
                          'S_JQL2_CODE': ['varchar(8)', '聚宽二级分类']}, 
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2005-01-01', '2030-12-31', freq='Y').to_list()}}
