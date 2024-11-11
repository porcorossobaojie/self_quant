# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 15:28:54 2021

@author: Porco Rosso
"""

class main():
    params = {'table': 'asharedescription', 
              'columns': {'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'], 
                          'S_INFO_COMPNAME': ['VARCHAR(16)', '股票名称'], 
                          'S_INFO_COMPNAMEENG': ['VARCHAR(16)', '股票名称_英文'], 
                          'S_INFO_LISTDATE': ['datetime', '上市日期'], 
                          'S_INFO_DELISTDATE': ['datetime', '退市日期']}
              }


