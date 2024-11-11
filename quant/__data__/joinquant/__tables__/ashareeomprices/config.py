# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:17 2021

@author: Porco Rosso
"""
import pandas as pd

class main():
    params = {'table': 'ashareeomprices', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'PCT_SIGN_TURN': ['double(24, 8)', '负面因子, 丢弃最小的10%'], 
                          'PCTDIFF_SIGN_TURN': ['double(24, 8)', '负面因子, 丢弃最小的10%'], 
                          'PCT_CORR': ['double(24, 8)', '涨跌幅'], 
                          'PCTDIFF_CORR': ['double(24, 8)', '涨跌幅'], 
                          'PUTU': ['double(24, 8)', '涨跌幅'], 
                          'PDTU': ['double(24, 8)', '涨跌幅'], 
                          'PDTD': ['double(24, 8)', '涨跌幅'], 
                          'PUTD': ['double(24, 8)', '涨跌幅'], 
                          'TURN_STD': ['double(24, 8)', '涨跌幅'], 
                          'TUDF_STD': ['double(24, 8)', '涨跌幅'], 
                          'PCT_SIGN_TURN_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PCTDIFF_SIGN_TURN_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PCT_CORR_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PCTDIFF_CORR_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PUTU_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PDTU_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PDTD_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'PUTD_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'TURN_STD_ADJ': ['double(24, 8)', '涨跌幅'], 
                          'TUDF_STD_ADJ': ['double(24, 8)', '涨跌幅'], 
                          },
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2017-01-01', '2030-12-31', freq='Y').to_list()}
              }
              

