# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:17 2021

@author: Porco Rosso
"""
import pandas as pd

class main():
    params = {'table': 'ashareorder', 
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'],
                          'S_DQ_NETMAIN': ['double(12, 2)', '主力净额(万)\n主力净额 = 超大单净额 + 大单净额'], 
                          'S_DQ_NETMAIN_PCT': ['double(8, 6)', '主力净占比\n主力净占比 = 主力净额 / 成交额'], 
                          'S_DQ_NETXL':['double(12, 2)', '超大单净额(万)	\n超大单:大于等于50万股或者100万元的成交单'], 
                          'S_DQ_NETXL_PCT': ['double(8, 6)', '超大单净占比\n超大单净占比 = 超大单净额 / 成交额'], 
                          'S_DQ_NETLRG': ['double(12, 2)', '大单净额(万)	\n大单:大于等于10万股或者20万元且小于50万股或者100万元的成交单'], 
                          'S_DQ_NETLRG_PCT': ['double(8, 6)', '大单净占比\n大单净占比 = 大单净额 / 成交额'], 
                          'S_DQ_NETMID': ['double(12, 2)', '中单净额(万)	\n中单:大于等于2万股或者4万元且小于10万股或者20万元的成交单'], 
                          'S_DQ_NETMID_PCT': ['double(8, 6)', '中单净占比\n中单净占比 = 中单净额 / 成交额'], 
                          'S_DQ_NETSML': ['double(12, 2)', '小单净额(万)	\n小单:小于2万股或者4万元的成交单'], 
                          'S_DQ_NETSML_PCT': ['double(8, 6)', '小单净占比\n小单净占比 = 小单净额 / 成交额'], },
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2010-01-01', '2030-12-31', freq='Y').to_list()}
              }
              

