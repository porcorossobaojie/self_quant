# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharebars180min.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        df1 = jq.get_bars(self.stock, fields=['open','close','low','high','volume','money', 'factor'], end_dt=date, unit='180m', count=1, include_now=True, fq_ref_date='2000-01-01')
        df1 = df1[df1['date'] == date]
        if df1.shape[0]:
            df = df1.reset_index(0)
            df['avg_price'] = df['money'] / df['volume']
            df['s_adj_open'] = df['open'] * df['factor']
            df['s_adj_close'] = df['close'] * df['factor']
            df['s_adj_avg_price'] = df['avg_price'] * df['factor']
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
        periods = pd.date_range(date if date is not None else '2014-01-01 14:00', pd.Timestamp.today(), freq='d')
        periods = periods[periods > date] if date is not None else periods
        if len(periods):
            for i in periods:
                if i.date() in self.trade_days.date:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                
if __name__ == '__main__':
    self = main()
    self.daily()    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
