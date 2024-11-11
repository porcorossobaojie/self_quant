# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 15:57:32 2021

@author: Porco Rosso
"""

class main():
    params = {'table': 'asharestatus', 
              'source_key': ['id', 'code', 'change_date', 'public_status_id'],
              'columns': {'ID_KEY': ['int', '来源自增id'],
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'TRADE_DT': ['datetime', '交易日'], 
                          'S_DQ_ST': ['int', '上市状态']}, 
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE']}