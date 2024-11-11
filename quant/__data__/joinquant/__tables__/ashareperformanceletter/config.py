# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 15:32:51 2023

@author: admin
"""

import pandas as pd

class main():
    params = {'table': 'ashareperformanceletter', 
              'columns': {'ID_KEY': ['INT', '来源自增ID'],
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'ANN_DT': ['datetime', '公告日'], 
                          'REPORT_PERIOD': ['datetime', '报告期'], 
                          'TOT_OPER_REV_LT': ['DECIMAL(20, 4)', '营业总收入'], 
                          'OPER_REV_LT':['DECIMAL(20, 4)', '营业收入'], 
                          'OPER_PROFIT_LT': ['DECIMAL(20, 4)', '营业利润'], 
                          'TOT_PROFIT_LT': ['DECIMAL(20, 4)', '利润总额'], 
                          'NET_PROFIT_PARENT_COMP_LT': ['DECIMAL(20, 4)', '归属于母公司所有者的净利润'], 
                          'TOT_ASSETS_LT': ['DECIMAL(20, 4)', '总资产'], 
                          'ROE_OWNER_LT': ['DECIMAL(20, 4)', '归属于上市公司股东的所有者权益'], 
                          'EPS_LT': ['DECIMAL(20, 4)', '归属于上市公司股东的每股净资产'], 
                          'ROA_LT': ['DECIMAL(20, 4)', '净资产收益(加权)'], },
              'primary': 'UNIQUE_KEY', 
              'keys': ['ANN_DT', 'REPORT_PERIOD'], 
              }
              