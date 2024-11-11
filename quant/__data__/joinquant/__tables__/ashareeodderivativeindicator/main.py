# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareeodderivativeindicator.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, date):
        df = jq.get_fundamentals(jq.query(jq.valuation), date=date.date())
        if df['turnover_ratio'].any():
            df = df.reindex(self.source_key, axis=1)
            df.columns = self.columns.keys()
            df = self.__code_replace__(df)
            df['TRADE_DT'] = pd.to_datetime(df['TRADE_DT']) + pd.Timedelta(15, 'h')
        else:
            df = pd.DataFrame(columns=self.columns.keys())
        return df
    
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
        periods = self.__days__(date)
        if len(periods):
            for i in periods:
                if i in self.trade_days:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
