# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 10:47:34 2021

@author: Porco Rosso
"""
from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharestatus.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
        
    def __source__(self, id_key):
        df = jq.finance.run_query(jq.query(jq.finance.STK_STATUS_CHANGE).order_by(jq.finance.STK_STATUS_CHANGE.id).filter((jq.finance.STK_STATUS_CHANGE.id > id_key) & ((jq.finance.STK_STATUS_CHANGE.public_status_id == 301001) | (jq.finance.STK_STATUS_CHANGE.public_status_id == 301002) | (jq.finance.STK_STATUS_CHANGE.public_status_id == 301003) | (jq.finance.STK_STATUS_CHANGE.public_status_id == 301005))).limit(5000))
        df = df.reindex(self.source_key, axis=1)
        df.columns = self.columns.keys()
        df = self.__code_replace__(df)
        df['TRADE_DT'] = pd.to_datetime(df['TRADE_DT']) + pd.Timedelta(15, 'h')
        df['S_DQ_ST'] = df['S_DQ_ST'].replace({301001: 0, 301002: 1, 301003: 2, 301005: 3})
        return df, df['ID_KEY'].max()
    
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        id_key = self.__command__('SELECT MAX(ID_KEY) FROM %s' %(self.table))[0][0]
        id_key = 0 if id_key is None else id_key
        while True:
            df, id_key = self.__source__(id_key)
            self.__write__(df)
            if len(df) < 5000:
                break























        