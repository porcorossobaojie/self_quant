# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:09:36 2021

@author: Porco Rosso
"""


from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharefinanceforcast.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, id_key):
        id_key = 0 if id_key is None else id_key
        df = jq.finance.run_query(jq.query(jq.finance.STK_FIN_FORCAST).order_by(jq.finance.STK_FIN_FORCAST.id).filter(jq.finance.STK_FIN_FORCAST.id > id_key))
        df = df.reindex(self.source_key, axis=1)
        df.columns = self.columns.keys()
        df = self.__code_replace__(df)
        df['ANN_DT'] = pd.to_datetime(df['ANN_DT']) + pd.Timedelta(15, 'h')
        return df, len(df), df['ID_KEY'].max()

    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        id_key = self.__command__('SELECT MAX(ID_KEY) FROM %s' %(self.table))[0][0]
        while True:
            df, lens, id_key = self.__source__(id_key)
            self.__write__(df)
            if lens < 5000:
                break













