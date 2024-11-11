# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 15:28:50 2021

@author: Porco Rosso

"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.asharedescription.config import main as config

import pandas as pd

class main(meta, type('config', (), config.params)):
        
    def __source__(self):
        df = jq.get_all_securities(['stock'], None)
        df = df.reset_index().drop('type', axis=1)
        df.columns = self.columns.keys()
        df = self.__code_replace__(df)
        df['S_INFO_DELISTDATE'][df['S_INFO_DELISTDATE'] >= pd.to_datetime(pd.Timestamp.today().date())] = pd.to_datetime(pd.Timestamp.today().date()) + pd.Timedelta(15 + 24 * 7, unit='h')
        return df
    
    def daily(self):
        df = self.__source__()
        self.__write__(df, 'replace')
        
asharedescription = main()
        
            
        
        






