# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:55:50 2023

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.america.config import main as config

import pandas as pd
import requests
import numpy as np

class main(meta, type('config', (), config.params)):
    def __source__(self, date=None):
        params = config.token_infomation.copy()
        params['trade_date__eq'] = pd.to_datetime(date).date().__str__()
        quote = requests.get(url=config.quote_url, params=params, verify=False)
        df = pd.DataFrame(quote.json())
        if len(df):
            df = df.rename(dict(zip(params['fields'].split(','), self.columns.keys())), axis=1)
            df['S_DQ_ADJAVGPRICE'] = (df[['S_DQ_ADJOPEN', 'S_DQ_ADJCLOSE', 'S_DQ_ADJLOW', 'S_DQ_ADJHIGH']] * [0.2,0.4,0.2,0.2]).sum(axis=1)
            df['S_DQ_AMOUNT'] = df['S_DQ_ADJAVGPRICE'] * df['S_DQ_ADJVOLUME']
            df['S_DQ_CAP'] = df['S_DQ_CAP'].replace(0, np.nan)
            df = df[df['S_DQ_CAP'] > 10000]
            df['S_DQ_TURNOVER'] = df['S_DQ_AMOUNT'] / df['S_DQ_CAP']
            df['TRADE_DT'] = pd.to_datetime(df['TRADE_DT'])  + pd.Timedelta(15, 'h')
        else:
            df = pd.DataFrame(columns = self.columns.keys())
        return df

    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
        date = '2015-01-01' if date is None else date
        periods = self.__days__(date)
        if len(periods):
            for i in periods:
                print(i)
                df = self.__source__(i)
                self.__write__(df)
                


