# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 09:59:48 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharedividend.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
        
    def __source__(self, id_key=None):
        id_key = self.__command__('SELECT MAX(ID_KEY) FROM %s' %(self.table))[0][0] if id_key is None else id_key
        id_key = 0 if id_key is None else id_key
        df = jq.finance.run_query(jq.query(jq.finance.STK_XR_XD).order_by(jq.finance.STK_XR_XD.id).filter((jq.finance.STK_XR_XD.id > id_key) & (jq.finance.STK_XR_XD.report_date >= '2004-01-01')))
        df = df[self.source_key]       
        df = df.rename(dict(zip(self.source_key, self.columns.keys())), axis=1)
        lens = len(df)
        id_key =  df['ID_KEY'].max()
        df = df[df[['REGISTRATION_DT', 'EX_DT', 'DVD_PAYOUT_DT', 'CANCEL_DT']].notnull().any(axis=1)]
        for i in df.columns:
            if i.split('_')[-1] == 'DT':
                df[i] = pd.to_datetime(df[i]) + pd.Timedelta(15, 'h')
        df['S_DIV_TOTAL'] = df[['S_DIV_BONUSRATE', 'S_DIV_CONVERSEDRATE']].sum(axis=1, min_count=1)
        df = self.__code_replace__(df)
        return df, lens, id_key
    
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__()
        id_key = self.__command__('SELECT MAX(ID_KEY) FROM %s' %(self.table))[0][0]
        while True:
            df, lens, id_key = self.__source__(id_key)
            self.__write__(df)
            if lens < 5000:
                break
            
asharedividend = main()        




