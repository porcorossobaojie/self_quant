# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareeodprices1min.config import main as config

import pandas as pd
import numpy as np

class main(meta, type('config', (), config.params)):
    trade_days = pd.to_datetime(jq.get_trade_days('2017-01-01')) + pd.Timedelta(15, 'h')
    def __source__(self, date=None):
        df = jq.get_price(self.stock, fields=['open','close','low','high','volume','money'], start_date=date - pd.Timedelta(6, 'h'), end_date=date, fq=None, skip_paused=True, frequency='5m')        
        df_day = jq.get_price(self.stock, fields=['open','close','low','high','volume','money', 'pre_close', 'low_limit', 'high_limit'], start_date=date - pd.Timedelta(6, 'h'), end_date=date, fq=None, skip_paused=True, frequency='1d')
        if df.shape[0]:
            df = pd.merge(df, df_day[['code', 'pre_close', 'low_limit', 'high_limit']], on='code')
            df = df.set_index(['time', 'code']).unstack().sort_index()
            dic = {}
            dic['pct'] = df['close'].pct_change()
            dic['pct'].iloc[0] = df['close'].iloc[0] / df['pre_close'].iloc[0] - 1
            dic = pd.concat(dic, axis=1)
            df = pd.concat([df, dic], axis=1)
            df = df.stack().reset_index()
            df = df.drop('pre_close', axis=1)
            df.columns = self.columns.keys()
            df = self.__code_replace__(df)
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
                if jq.get_query_count()['spare'] < 2000000:
                    print('not enough query from join data')
                    break
                if i in self.trade_days:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
