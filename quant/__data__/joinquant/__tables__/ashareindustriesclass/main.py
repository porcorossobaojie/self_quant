# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 10:10:16 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareindustriesclass.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    stock = jq.get_all_securities().index.to_list()
    def __source__(self, date):
        df = jq.get_industry(self.stock, date=date)
        df = [pd.DataFrame(j).iloc[0].rename(i) for i,j in df.items() if len(j)]
        df = pd.concat(df, axis=1).T
        df.index.name = 'S_INFO_WINDCODE'
        columns = {'sw_l1': 'S_SWL1_CODE', 'sw_l2': 'S_SWL2_CODE', 'sw_l3': 'S_SWL3_CODE', 'jq_l1': 'S_JQL1_CODE', 'jq_l2': 'S_JQL2_CODE'}
        df = df.rename(columns, axis=1).reindex(columns.values(), axis=1).dropna(how='all')
        df = df.reset_index()
        df = self.__code_replace__(df)
        df['TRADE_DT'] = date
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
                    
    def detail(self):
        df = jq.get_industry(self.stock)
        df = [pd.DataFrame(j).unstack().rename(i) for i,j in df.items() if len(j)]
        df = pd.concat(df, axis=1)
        df = df.iloc[:-2]
        df.index = ['S_JQL1_CODE', 'S_JQL1_DETAIL', 'S_JQL2_CODE', 'S_JQL2_DETAIL', 'S_SWL1_CODE', 'S_SWL1_DETAIL', 'S_SWL2_CODE', 'S_SWL2_DETAIL', 'S_SWL3_CODE', 'S_SWL3_DETAIL', ]
        df.columns.name = 'S_INFO_WINDCODE'
        df = df.T.dropna(how='all').reset_index()
        df = self.__code_replace__(df)
        return df














