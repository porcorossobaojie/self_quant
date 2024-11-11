# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 09:34:16 2021

@author: lenovo
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.aindexeodprices1min.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    trade_days = pd.to_datetime(jq.get_trade_days('2017-01-01')) + pd.Timedelta(15, 'h')
    def __source__(self, date=None):
        df = jq.get_price(self.security, fields=self.fields, start_date=date - pd.Timedelta(6, 'h'), end_date=date, fq=None, skip_paused=True, frequency='1m') 
        df = df.rename(dict(zip(['time', 'code'] + self.fields, self.columns.keys())), axis=1)
        df['S_DQ_PCTCHANGE'] = df['S_DQ_CLOSE'] / df['S_DQ_PRECLOSE'] - 1
        df = self.__code_replace__(df)
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
                






















