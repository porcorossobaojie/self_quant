# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:09:56 2021

@author: Porco Rosso
"""

import pandas as pd

class meta():
        
    def __init__(self, begin, end=None):
        [setattr(self, i.__name__, i(filter_min=pd.to_datetime(begin), filter_max=pd.to_datetime(end) if end is not None else end)) for i in self.__tables__]
        
    def __call__(self, keys, name=None, end=None, quarter=False, shift=None):
        if isinstance(keys, str):
            keys = keys.upper()
            attr = self._help[self._help['COLUMN_NAME'].isin([keys])]
        else:
            keys = [i.upper() for i in keys]
            attr = self._help[self._help['COLUMN_NAME'].isin(keys)]
        table = attr['TABLE_NAME'].unique()
        if len(table) == 1:
            source = getattr(self, table[0])
            return source(keys, name, end, quarter, shift)
        elif len(table) < 1:
            raise ValueError('keys is not exist')
        else:
            raise ValueError('table had keys is not unique')
