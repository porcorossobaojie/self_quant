# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharebars1min.config import main as config

import pandas as pd
import datetime

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        if date.date() == pd.Timestamp.today().date() and date.hour <= 16:
            df1 = jq.get_bars(self.stock, fields=['open','close','low','high','volume','money'], end_dt=date + pd.Timedelta(1, 'min'), unit='1m', count=1, include_now=False)
            df1 = df1[df1['date'] == date]
        else:
            f1 = jq.get_price(self.stock, fields=['open','close','low','high','volume','money'], end_date=date, fq=None, skip_paused=True, count=1, frequency='1m')   
            
        if df1.shape[0]:
            df = df1.reset_index(0)
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
        periods = pd.date_range(date if date is not None else '2014-01-01 09:30', pd.Timestamp.today(), freq='1min')
        periods = periods[(periods.time >= datetime.time(9, 30)) & (periods.time <= datetime.time(11, 30)) | (periods.time >= datetime.time(13, 0)) & (periods.time <= datetime.time(15, 0))]
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
