# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 20:38:30 2021

@author: Porco Rosso
"""

import pandas as pd

class main():
    params = {'security': ['000852.XSHG', '000905.XSHG', '399300.XSHE'],
              'fields': ['date', 'weight'],
              'table': 'aindexhs300freeweight', 
              'columns': {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'REPORT_PERIOD': ['datetime', '报告日期'], 
                          'S_DQ_WEIGHT': ['double(6, 4)', '权重'], 
                          'S_INFO_INDCODE': ['VARCHAR(16)', '指数代码'],
                          'ANN_DT': ['datetime', '报告期']
                          },
              'primary': 'UNIQUE_KEY', 
              'keys': ['ANN_DT', 'S_INFO_WINDCODE'], 
              }