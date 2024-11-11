# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 16:12:12 2021

@author: Porco Rosso
"""
from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharecashflow.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, id_key):
        df = jq.finance.run_query(jq.query(jq.finance.STK_CASHFLOW_STATEMENT).order_by(jq.finance.STK_CASHFLOW_STATEMENT.id).filter((jq.finance.STK_CASHFLOW_STATEMENT.source_id == 321003) & (jq.finance.STK_CASHFLOW_STATEMENT.report_type == 0) & (jq.finance.STK_CASHFLOW_STATEMENT.id > id_key)).limit(5000))
        df = df.loc[:, df.columns.isin(config.information['source_key'])]
        df = df.rename(dict(config.information[['source_key', 'save_key']].values), axis=1)
        df.columns = df.columns.str.upper()
        df = self.__code_replace__(df)
        df['ANN_DT'] = pd.to_datetime(df['ANN_DT']) + pd.Timedelta(15, 'h')
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
