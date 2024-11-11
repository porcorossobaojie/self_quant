# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 17:45:54 2022

@author: Porco Rosso
"""

import flow
from __factors__ import barra

from __factors__.base.main import main as meta
from __factors__.equity.config import main as config
from __pandas.__stats.__obj import __neutral as neutral
import pandas as pd
import numpy as np

class main(meta):
        
    def data_init(self):
        self.initialize(**config.params)
        
    
    def _log(self, df, abs=True, add=1):
        df = (np.sign(df) if abs else 1) * np.log((df.abs() if abs else df) + add)
        return df
    
    def _finance_standard(self, key, shift, fillna, log, **kwargs):
        df = flow.stock_finance(key, shift=shift, **kwargs)
        df = df.fillna(fillna)                
        if log:
            df = self._log(df)
        return df

    def _finance_gth(self, key, shift, fillna, log, periods, **kwargs):
        df = self._finance_standard(key, shift, np.nan, log, periods=periods, **kwargs)
        df = df.groupby(df.index.names[0]).fillna(method='ffill', limit=periods-2)
        if log:
            df = df.groupby(df.index.names[0]).diff()
        else:
            df = df.groupby(df.index.names[0]).pct_change(fill_method=None)
            df = df[df.abs() != np.inf]
        df = df[df.index.get_level_values(1) == periods]
        df.index = df.index.get_level_values(0)
        df = df.fillna(fillna)
        return df
    
    def Fac_mv(self, key='s_dq_mv', log=True):
        df = flow.stock(key)
        if log:
            df = self._log(df)
        return df
    
    def Fac_assets_LIAB(self):
        key = {
                'assets': 'TOT_ASSETS', 
                'liab': 'TOT_LIAB',
                'cur_assets': 'TOT_CUR_ASSETS',
                'cur_liab': 'TOT_CUR_LIAB',
                'tot_profit':'TOT_PROFIT',
                'oprt_profit':'OPER_PROFIT'
                }
        params = {
                'shift': 4,
                'log': False,
                'periods': 12,
                'fillna': np.nan
                }   
        df_dic = {j: self._finance_standard(j, **params) for i,j in key.items()}
        df = pd.concat(df_dic, axis=1)
        facs = df[df.index.get_level_values('PERIODS') == params['periods']]
        facs.index = facs.index.droplevel('PERIODS')
        facs = np.log(facs)
        facs = facs.stack()
        gth = df.groupby('TRADE_DT').pct_change(fill_method=None)
        unexcept = gth[gth.index.get_level_values('PERIODS') == params['periods']]
        unexcept.index = unexcept.index.droplevel('PERIODS')
        unexcept = (unexcept - gth.groupby('TRADE_DT').mean()) / gth.groupby('TRADE_DT').std()
        hold = gth.notnull().groupby('TRADE_DT').sum()
        unexcept = unexcept[hold >= 4]
        unexcept = unexcept.stack()
        unexcept.columns = unexcept.columns + '_GTH'
        facs = pd.concat([facs, unexcept], axis=1)
        return facs
    
    def evaluate(self, fac_df):
        facs_sorts = fac_df.columns[~fac_df.columns.str.contains('_GTH')]
        df = pd.concat([self.Fac_mv().stack().to_frame('MV'), flow.stock('s_jql1_code').stack().to_frame('IND'), fac_df], axis=1)
        df = df.unstack()
        dic = {}
        for date, temp_df in df.iterrows():
            temp_df = temp_df.unstack(0).dropna().stats.const(['IND'])
            if len(temp_df) > 1000:
                temp_dic = {}
                for key in facs_sorts.to_list() + ['MV']:
                    ttemp_df = temp_df.sort_values(key, ascending=False)
                    temp = ttemp_df[facs_sorts].rolling(500, center=True, min_periods=250).mean()
                    temp = ttemp_df[facs_sorts] / temp
                    temp.columns = temp.columns + ['_DIFF']
                    ttemp_df = pd.concat([ttemp_df, temp], axis=1)
                    temp_lst = []
                    for i in range(len(ttemp_df) - 500):
                        ols_df = ttemp_df.iloc[i: 500 + i]
                        ols = ols_df.stats.OLS(True).resid
                        temp_lst.append(ols)
                    temp_lst = pd.concat(temp_lst, axis=1)
                    temp_lst = (ttemp_df['MV'] - temp_lst.mean(axis=1))
                    temp_dic[key] = temp_lst
                temp_dic = pd.concat(temp_dic, axis=1)
                dic[date] = temp_dic
                print(date)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


