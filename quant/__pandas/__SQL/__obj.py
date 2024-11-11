# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:58:40 2020

@author: Porco Rosso
"""

import pandas as pd
from __pandas.__SQL.config import __obj as config

def _write(x, schemas, table, exist='append', index=False, logs=False, **kwargs):
    log = getattr(pd, config.pandasAttrName).login
    con = log.__engine__(schemas=schemas, **kwargs)
    x.to_sql(table, con=con, if_exists=exist, index=index, chunksize=160000)
    con.dispose()
    if logs is True:
        print('Write DataFrame in ' + schemas + '.' + table + 'logs %s records.' %(len(x)))

@pd.api.extensions.register_dataframe_accessor(config.pandasAttrName)
class SQL():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        
    def write(self, schemas, table, exist='append', index=False, information=False, **kwargs: "'charset', 'port', 'user', 'password', 'host'"):
        '''
        ------------
        
        Explain:
            write dataframe into MySQL by parameters.
        
        ------------
        
        Parameters:
            
            schemas:
                str.
                schemas name.
                
            tabel:
                str.
                table name.
                
            exist:
                str in {'append', 'replace', 'fail'}.
                append: append new data into old table.
                replace: cover old table by new data.
                fail: raise error.
                
            index:
                bool.
                whether save dataframe.index into MySQL.
                
            information:
                bool.
                whether print save login information.
                
            kwargs:
                user, password, host, port if needed.
                
        ------------
        
        Returns:
            /
        
        ------------
        '''
        _write(self._obj, schemas, table, exist, index, information, **kwargs)   
