# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 15:11:40 2021

@author: Porco Rosso
"""

import pandas as pd
import __pandas
from __data__.joinquant import joinquant as jq

from __data__.joinquant.__tables__.meta.config import meta as config

class meta(pd.SQL.__login__):
    stock = jq.get_all_securities('stock', date=None).index.tolist()   
    trade_days = pd.to_datetime(jq.get_trade_days('2005-01-01')) + pd.Timedelta(15, 'h')
    def __init__(self, **kwargs):
        params = config.params.copy()
        params.update(**kwargs)
        super().__init__(**params)
        
    def __source__(self):
        pass
        
    def __code_replace__(self, df):
        df['S_INFO_WINDCODE'] = df['S_INFO_WINDCODE'].str.replace('XSHG', 'SH')
        df['S_INFO_WINDCODE'] = df['S_INFO_WINDCODE'].str.replace('XSHE', 'SZ')
        return df
        
    def __days__(self, begin=None):
        begin = '2005-01-01 15:00' if begin is None else begin
        obj = pd.date_range(begin, pd.Timestamp.today())
        obj = obj[1:] if len(obj) else obj
        if len(obj) and (obj[-1].day == pd.Timestamp.today().day and pd.Timestamp.today().hour < 19):
            obj = obj[:-1]
        return obj
    
    def __write__(self, df, exist='append'):
        if exist == 'replace':
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table), self.schemas)
            self.__create__()
        if exist == 'append':
            if not self.__exist__():
                self.__create__()
        df.SQL.write(self.schemas, self.table)
        print('%s records write sucessed in %s.%s' %(len(df), self.schemas, self.table))


