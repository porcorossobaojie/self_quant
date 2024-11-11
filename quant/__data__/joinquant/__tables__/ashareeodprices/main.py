# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareeodprices.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        df1 = jq.get_price(self.stock, fields=['open','close','low','high','volume','money', 'high_limit','low_limit','avg','pre_close','paused'], start_date=date, end_date=date, fq=None, skip_paused=False).drop('time', axis=1).set_index('code')    
        if df1.shape[0]:
            df3 = jq.get_price(self.stock, fields=['factor'], start_date=date, end_date=date, fq='post', skip_paused=False).drop('time', axis=1).set_index('code')   
            df3[['open', 'close', 'avg', 'pre_close']] = df1[['open', 'close', 'avg', 'pre_close']].mul(df3['factor'], axis=0)
            df3['S_DQ_PCTCHANGE'] = df3['close'] / df3['pre_close'] - 1
            df = pd.concat([df1, df3], axis=1).reset_index()
            df.insert(0, 'TRADE_DT', pd.to_datetime(pd.to_datetime(date).date()) + pd.Timedelta(15, 'h'))
            df.columns = self.columns.keys()
            df = self.__code_replace__(df)
            df = df[df.isnull().sum(axis=1) < 10]
            df['S_DQ_TRADESTATUS'] = ~df['S_DQ_TRADESTATUS'] .astype(bool)
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
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
