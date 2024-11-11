# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 20:38:36 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.aindexhs300freeweight.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        lst = []
        for i in self.security:
            df = jq.get_index_weights(i, date=date)[self.fields]
            df.index.name = 'code'
            df['index'] = i.replace('XSHG', 'SH').replace('XSHE', 'SZ')
            lst.append(df.reset_index())
        df = pd.concat(lst)
        if len(df):
            
            df = df.rename(dict(zip(['code'] + self.fields + ['index'], self.columns.keys())), axis=1)
            df['ANN_DT'] = pd.to_datetime(date.date())  + pd.Timedelta(15, 'h')
            df = self.__code_replace__(df)
        return df

    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        date = self.__command__('SELECT MAX(ANN_DT) FROM %s' %(self.table))[0][0]
        periods = self.__days__(date)
        date = periods[0] if len(periods) and date is None else date
        if len(periods):
            for i in periods:
                if i in self.trade_days and i.month != date.month:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                    date = i
                

