# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:55:45 2022

@author: Porco Rosso
"""

class main():
    table_info = [{'schemas':'join_data',
                  'table': 'ashareeodprices', 
                  'columns': ['TRADE_DT', 'S_INFO_WINDCODE', 'S_DQ_OPEN', 'S_DQ_LOW', 'S_DQ_HIGH', 'S_DQ_CLOSE', 'S_DQ_AVGPRICE', 'S_DQ_HIGH_LIMIT', 'S_DQ_LOW_LIMIT', 'S_DQ_ADJPRECLOSE', 'S_DQ_TRADESTATUS', 'S_DQ_ADJCLOSE', 'S_DQ_ADJAVGPRICE', 'S_DQ_ADJOPEN', 'S_DQ_PCTCHANGE', 'S_DQ_POST_FACTOR'],
                  'where': 'TRADE_DT >= "2014-01-01"'},
                  {'schemas': 'join_data', 
                   'table':'asharestatus', 
                   'columns':['TRADE_DT', 'S_INFO_WINDCODE', 'S_DQ_ST']}, 
                  ]
    
    














