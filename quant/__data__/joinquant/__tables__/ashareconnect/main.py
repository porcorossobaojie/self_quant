# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareconnect.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        date = date.date().__str__()
        df1 = jq.finance.run_query(jq.query(jq.finance.STK_HK_HOLD_INFO).filter(jq.finance.STK_HK_HOLD_INFO.day==date)).loc[:, ['day', 'code', 'link_id', 'share_number', 'share_ratio']]    
        if df1.shape[0]:
            df1.columns = self.columns.keys()
            df1 = self.__code_replace__(df1)
            df1.iloc[:,0] = pd.to_datetime(pd.to_datetime(date).date()) + pd.Timedelta(15, 'h')
            df1.iloc[:, -1] = df1.iloc[:, -1] / 100
        else:
            df1 = pd.DataFrame(columns=self.columns.keys())
        return df1
    
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
        date = '2017-02-28 15:00' if date is None else date
        periods = self.__days__(date)
        if len(periods):
            for i in periods:
                if i in self.trade_days:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
