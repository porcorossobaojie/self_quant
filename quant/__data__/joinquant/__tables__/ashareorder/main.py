# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareorder.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        df1 = jq.get_money_flow(self.stock, fields=['date', 'sec_code', 'net_amount_main', 'net_pct_main', 'net_amount_xl', 'net_pct_xl', 'net_amount_l', 'net_pct_l', 'net_amount_m', 'net_pct_m', 'net_amount_s', 'net_pct_s'], start_date=date, end_date=date)    
        if df1.shape[0]:
            df1.loc[:, df1.columns.str.contains('pct')] = df1.loc[::, df1.columns.str.contains('pct')] / 100
            df1.iloc[:, 0] = date
            df1.columns = self.columns.keys()
            df1 = self.__code_replace__(df1)
        else:
            df1 = pd.DataFrame(columns=self.columns.keys())
        return df1
    
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
        date = '2010-01-01 15:00' if date is None else date
        periods = self.__days__(date)
        if len(periods):
            for i in periods:
                if i in self.trade_days:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
