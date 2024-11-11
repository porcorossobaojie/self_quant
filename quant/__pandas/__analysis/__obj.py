# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 11:21:57 2022

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
from __pandas.__analysis.config import __obj as config


def _maxdown(df_obj, iscumprod):
    if not iscumprod:
        x = df_obj.add(1, fill_value=0).cumprod()
        x[df_obj.isnull()] = pd.NA
    else:
        x = df_obj
    max_flow = x.expanding(min_periods=1).max()
    down_date = (x / max_flow).idxmin()
    max_down = x / max_flow - 1
    down_infomations = [(x.loc[j, i] if pd.notnull(j) else np.nan, max_down.loc[j, i] if pd.notnull(j) else np.nan) for i, j in down_date.iteritems()]
    down_value, max_down = list(zip(*down_infomations))
    up_value = pd.Series([max_flow.loc[j, i] if pd.notnull(j) else np.nan for i, j in down_date.iteritems()], index=down_date.index)
    up_date = max_flow[max_flow == up_value].idxmin()
    df = pd.DataFrame([up_date.values, up_value, down_date.values, down_value, max_down], columns=df_obj.columns, index=['Maxdown_Start_Date', 'Maxdown_Start_Value', 'Maxdown_End_Date', 'Maxdown_End_Value', 'Maxdwon_Percent'])
    return df

def _sharpe(df_obj, iscumprod, periods):
    x =  df_obj if not iscumprod else df_obj.pct_change(fill_method=None)
    y = x.mean() / x.std()
    if periods is not None:
        periods = min([len(x), periods])
        y = y * periods ** 0.5
    y.name = 'periods in %s' %(periods)
    return y

def _effective(df_obj, group_adj):
    x = df_obj.diff(axis=1)
    x = np.sign(x) * x ** 2
    x = x.sum(axis=1)
    x = x * (df_obj.shape[1] - 1) ** 0.5 if group_adj else x
    return x

def _rank_on(df_obj, factor, weight, axis):
    factor = factor.rank(axis=axis, pct=True).reindex_like(df_obj)[df_obj.notnull()]
    if weight is not None:
        weight = weight.reindex_like(df_obj)[df_obj.notnull()]
        weight = weight.div(weight.sum(axis=axis, min_count=1), axis=int(~bool(axis)) + 2)
        factor = (factor * weight).sum(axis=axis, min_count=1)
    else:
        factor = factor.mean(axis=axis)
    return factor

def _expose(df_obj, weight, low_bound, up_bound, **factors):
    if not len(factors):
        raise ValueError()
    else:
        factors = {i:(j.rank(axis=1, pct=True) - 0.5) for i,j in factors.items()}
    if weight is not None:
        weight = weight.reindex_like(df_obj)[df_obj.notnull()]
        weight = weight.div(weight.sum(axis=1, min_count=1), axis=0)
        rank = {i:(j.reindex_like(df_obj)[df_obj.notnull()] * weight).sum(axis=1, min_count=1) for i,j in factors.items()}
    else:
        rank = {i: j[df_obj.notnull()].mean(axis=1) for i,j in factors.items()}
    if low_bound is not None and up_bound is not None:
        bound = pd.concat({i:pd.concat({'low': j - low_bound, 'up': j + up_bound}, axis=1) for i,j in rank.items()}, axis=1)
    else:
        bound = None
    x = type('rank_obj', (), {'expose':pd.concat(rank, axis=1), 'factors':pd.concat(factors, axis=1), 'bound':bound})
    return x
    
    
    
    
    
    

@pd.api.extensions.register_series_accessor(config.pandasAttrName)
class analysis():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        
    def maxdown(self, iscumprod=False):
        '''
        ------------
        
        Explain:
            calculate the max down happen information.
        
        ------------
        
        Parameters:
        
            cumprod:
                bool.
                whether cumprod values with ' + 1 ' or not.
        
        ------------
        
        Returns:
            series.
            series of data[highest day, highest value, lowest day, lowest value, max down value]
        
        ------------
        '''
        return _maxdown(self._obj.to_frame(), iscumprod=iscumprod)

    def sharpe(self, iscumprod=False, periods=252):
        '''
        ------------
        
        Explain:
            calculate sharpe ratio.
        
        ------------
        
        Parameters:
        
            cumprod:
                bool.
                whether cumprod values with ' + 1 ' or not.
            
            periods:
                int.
                whether adjust dataframe sharpe ratio in periods.
        
        ------------
        
        Returns:
            series.
            
        ------------
        '''
        return _sharpe(self._obj.to_frame(), iscumprod, periods)
    
@pd.api.extensions.register_dataframe_accessor(config.pandasAttrName)
class analysis():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def maxdown(self, iscumprod=False):
        '''
        ------------
        
        Explain:
            calculate the max down happen information.
        
        ------------
        
        Parameters:
        
            cumprod:
                bool.
                whether cumprod values with ' + 1 ' or not.
        
        ------------
        
        Returns:
            series.
            series of data[highest day, highest value, lowest day, lowest value, max down value]
        
        ------------
        '''
        return _maxdown(self._obj, iscumprod=iscumprod)

    def sharpe(self, iscumprod=False, periods=252):
        '''
        ------------
        
        Explain:
            calculate sharpe ratio.
        
        ------------
        
        Parameters:
        
            cumprod:
                bool.
                whether cumprod values with ' + 1 ' or not.
            
            periods:
                int.
                whether adjust dataframe sharpe ratio in periods.
        
        ------------
        
        Returns:
            series.
            
        ------------
        '''
        return _sharpe(self._obj, iscumprod, periods)
    
    def effective(self, group_adj=False):
        '''
        ------------
        
        Explain:
            descrbie factor effectiveness by calculate group returns different.
        
        ------------
        
        Parameters:
        
            group_adj:
                bool.
                whether adjust result by group counts.
            
        ------------
        
        Returns:
            series.
            
        ------------
        '''
        
        return _effective(self._obj, group_adj=group_adj)
    
    def rank_on(self, factor, weight=None, axis=1, adj=-0.5):
        '''
        ------------
        
        Explain:
            calculate factor expose rank which 0 is neutral
        
        ------------
        
        Parameters:
        
            factor:
                dataframe.
                factor for calculating exposed on.
                
            axis:
                int.
            
            weight:
                dataframe.
                weight information if exist.
        
        ------------
        
        Returns:
            series.
            
        ------------
        '''
        x = _rank_on(self._obj, factor, axis=axis, weight=weight) + adj
        return x
    
    def expose(self, weight=None, low_bound=None, up_bound=None, **factors):
        '''
        ------------
        
        Explain:
            calculate factors rank values.
            calculate factors expose rank which 0 is neutral.
            calculate factors bound range.
        ------------
        
        Parameters:
        
            weight:
                dataframe.
                weight information if exist.
        
            low_bound:
                float.
                low bound limit.
                
            up_bound:
                float.
                up bound limit.
        
            **factors:
                dataframe.
                factor for calculating exposed on.
                
        ------------
        
        Returns:
            class obj.
                cls.factors for ranked factors values.
                cls.expose for self exposed on factors.
                cls.bound for self.bound range.
            
        ------------
        '''
        
        x = _expose(self._obj, weight, low_bound, up_bound, **factors)
        return x
    
    def close_to(self, rank_obj, low_bound, up_bound, bound_weight):
        x = _close_to(self._obj, rank_obj, low_bound, up_bound, bound_weight)
        return x

