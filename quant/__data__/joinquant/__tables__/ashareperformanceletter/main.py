# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 16:12:12 2021

@author: Porco Rosso
"""
from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareperformanceletter.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
    def __source__(self, id_key):
        df = jq.finance.run_query(jq.query(jq.finance.STK_PERFORMANCE_LETTERS).order_by(jq.finance.STK_PERFORMANCE_LETTERS.id).filter((jq.finance.STK_PERFORMANCE_LETTERS.report_type == 0) & (jq.finance.STK_PERFORMANCE_LETTERS.id > id_key)).limit(5000))
        df = df[['id', 'code', 'pub_date','report_date', 'total_operating_revenue', 'operating_revenue', 'operating_profit','total_profit', 'np_parent_company_owners', 'total_assets','equities_parent_company_owners', 'basic_eps', 'weight_roe']]
        df['weight_roe'] = df['weight_roe'] / 100
        df.columns = self.columns.keys()
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
