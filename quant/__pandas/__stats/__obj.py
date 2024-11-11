# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 09:42:25 2019

@author: Porco Rosso
"""

import numpy as np
import scipy as sp
import pandas as pd
import statsmodels.api as sm
from __pandas.__stats.config import __obj as config

def _standard(df_obj, method='gauss', rank=(-3,3), axis=None):
    axis = 0 if axis is None else axis
    if method == 'gauss':
        y = df_obj.sub(df_obj.mean(axis=axis), axis=0 if axis or isinstance(df_obj, pd.Series) else 1).div(df_obj.std(axis=axis), axis=0 if axis or isinstance(df_obj, pd.Series) else 1)
        y = y.clip(*rank)
    elif method == 'uniform':
        y = df_obj.rank(pct=True, axis=axis)
        rank = (0 if rank[0] is None else rank[0], 1 if rank[1] is None else rank[1])
        y = y * (rank[1] - rank[0]) + rank[0]
    return y

def _OLS(df_obj, const=False, roll=None, min_periods=None, dropna=True, keys=(0, -1), returns=dict, weight=None):
    df = df_obj.copy()
    roll = len(df) if roll is None or roll > len(df) else roll
    min_periods = 0 if min_periods is None else min_periods
    df.insert(1, 'const', 1) if const is True else None
    dic = {}
    for i in range(len(df) - roll + 1):
        y = df.iloc[i: i + roll]
        w = weight.iloc[i : i + roll] if weight is not None else 1.0
        key = y.index[keys[1]] if keys[0] == 0 else y.columns[keys[1]]
        if len(y.dropna()) >= min_periods:
            dic[key] = sm.WLS(y.iloc[:, 0].astype(float), y.iloc[:,1:].astype(float), weights=w, missing='drop').fit()
        elif dropna == False:
            dic[key] = None
        if returns is dict:
            return dic
    if isinstance(returns, dict):
        return dic
    else:
        dic = list(dic.values())
        if len(dic) == 1:
            dic = dic[0]
        return dic
        
def _const(df_obj, columns=None, prefix=None, sep=''):
    return pd.get_dummies(df_obj, prefix=prefix, prefix_sep=sep, columns=columns)

def __neutral(array_3D):
    def cals(x):
        matrix = np.unique(x[~np.isnan(x).any(axis=1), :], axis=0)
        if (matrix.shape[0] > matrix.shape[1] * 2) and matrix.shape[0] > 5:
            x = matrix[:, 1:]
            xT = x.T
            y =  matrix[:, 0]
            params = sp.linalg.pinv(xT.dot(x)).dot(xT).dot(y)
            #params = np.linalg.pinv(xT.dot(x)).dot(xT).dot(y)
        else:
            params = np.array([np.nan] * (x.shape[1] - 1))
        return params
    params = np.array(list(map(cals, array_3D)))
    return params

def _neutral(df_obj, const=True, returns=['params', 'resid'], roll=None, roll_axis=0, neu_axis=0, **key_dfs):
    dict_array = {i:j.reindex_like(df_obj).values for i,j in key_dfs.items()}
    values = np.array([df_obj.values, np.ones_like(df_obj.values), *dict_array.values()]) if const else np.array([df_obj.values, *dict_array.values()])
    values = values.transpose(1 if neu_axis else 2, 2 if neu_axis else 1, 0)
    params_cols = (['const'] if const else []) + list(dict_array.keys())
    params_inds = df_obj.index if neu_axis else df_obj.columns
    
    def bar(v, end):
        class neutral_object():
            pass
        x = __neutral(v)
        if 'params' in returns:
            neutral_object.params = pd.DataFrame(x, index=params_inds[end -  x.shape[0] : end] if neu_axis != roll_axis else params_inds, columns=params_cols)
        if 'resid' in returns:
            resid = v[:, :, 0] - (v[:,:,1:] * x[:, np.newaxis, :]).sum(axis=2)
            resid = resid if neu_axis else resid.T
            index = df_obj.index if roll_axis else df_obj.index[end -  resid.shape[0] : end]
            columns = df_obj.columns[end -  resid.shape[1] : end] if roll_axis else df_obj.columns
            neutral_object.resid = pd.DataFrame(resid, index=index, columns=columns)
        return neutral_object
    
    if roll is None:
        obj = bar(values, end=df_obj.shape[roll_axis])
        return obj
    else:
        obj = {}
        iter_index = df_obj.columns if roll_axis else df_obj.index
        roll_on = 0 if values.shape[0] == len(iter_index) else 1
        for i, j in enumerate(iter_index[roll:], roll):
            input_array = values[:, i - roll : i, :] if roll_on else values[i - roll : i, :, :]
            obj[j] = bar(input_array, i)
        return obj
            
    
@pd.api.extensions.register_series_accessor(config.pandasAttrName)
class series_stats():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
    def standard(self, method='gauss', rank=(-5,5)):
        '''
        ------------
        
        Explain:
            standard series by parameters.
        
        ------------
        
        Parameters:
        
            method:
                {gauss, uniform}.
                gauss, standard series as N ~ (0, 1).
                uniform, standard series as uniform .
            
            rank:
                tuple / list.
                2d arrays which limit lowest and highest when standarding.
        
        ------------
        
        Returns:
            series.
        
        ------------
        '''
        return _standard(self._obj, method=method, rank=rank, axis=None)
    
    def const(self, prefix=None, sep=''):
        '''
        ------------
        
        Explain:
            dummy values in series to one-hot matrix.
        
        ------------
        
        Parameters:
        
            perfix:
                str / None.
                the str which add on new dataframe's columns.
            
            sep:
                str.
                the sep which between prefix and unique series values.
        
        ------------
        
        Returns:
            dataframe.
            one-hot matrix.
        
        ------------
        '''
        return _const(self._obj, prefix=prefix, sep=sep)
    
    def lp(self, low=0, up=0.01, sense='max', fac_dic=None, fac_pcted=True):
        if sense == 'max':
            sense = -1
        elif sense == 'min':
            sense = 1
        return _lp(self._obj, low, up, sense, fac_dic, fac_pcted, True)

@pd.api.extensions.register_dataframe_accessor(config.pandasAttrName)
class dataframe_stats():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
    def standard(self, method='gauss', rank=(-5,5), axis=1):
        '''
        ------------
        
        Explain:
            standard dataframe by parameters.
        
        ------------
        Parameters:
        
            method:
                {gauss, uniform}.
                gauss, standard series as N ~ (0, 1).
                uniform, standard series as uniform .
            
            rank:
                tuple / list.
                2d arrays which limit lowest and highest when standarding.
            
            axis:
                {0, 1}, recommand 0.
                the axis standard to.
        
        ------------
        
        Returns:
            dataframe.
        
        ------------
        '''
        x = _standard(self._obj, method=method, rank=rank, axis=axis)
        return x
    
    def const(self, columns=None, prefix=None, sep=''):
        '''
        ------------
        
        Explain:
            dummy values in series to one-hot matrix.
        
        ------------
        
        Parameters:
            
            columns:
                iterable.
                the names in dataframe's columns which needed turn to one-hot matrix.
            
            perfix:
                str list / None.
                the str which add on new dataframe's columns.
            
            sep:
                str.
                the sep which between prefix and unique series values.
        
        ------------
        
        Returns:
            dataframe.
            one-hot matrix.
        
        ------------
        '''
        return _const(self._obj, columns=columns, prefix=prefix, sep=sep)
    
    def OLS(self, const=False, roll=None, min_periods=None, dropna=True, keys=(0, -1), returns=list, weight=None):
        '''
        ------------
        
        Explain:
            do OLS on dataframe.
        
        ------------
        
        Parameters:
        
            const:
                bool.
                whether insert const in dataframe.
            
            roll:
                int / None.
                rolling OLS by roll as sample number.
            
            minPeriod:
                int / None.
                the minimum number allow to OLS.
            
            dropNone:
                bool.
                when it failed for OLS, whether hold the key with value(None) or not.
            
            keys:
                tuple / list in 2d arrays.
                keys[0], the axis we use for keys.
                keys[1], the key postion we choosen from.
            
            returns:
                {dict, list}.
                whether returns {keys: OLS objects} or [OLS objects]
        
        ------------
        
        Returns:
            dict / list of OLS objects.
        
        ------------
        '''
        return _OLS(self._obj, const=const, roll=roll, min_periods=min_periods, dropna=dropna, keys=keys, returns=returns, weight=weight)

    def neutral(self, const=True, returns=['params', 'resid'], roll=None, roll_axis=0, neu_axis=0, *df_objs, **key_dfs):
        '''
        ------------
        
        Explain:
            do neutral on dataframe by oth_objs and oth_kobjs.
        
        ------------
        
        Parameters:
        
            const:
                bool.
                whether insert const in doing neutral.
            returns:
                {params, resid}.
                return neutral params or resid or both.
        
        ------------
        
        Returns:
            tuple of DataFrame.
        
        ------------
        '''
        return _neutral(self._obj, const=const, returns=returns, roll=roll, roll_axis=roll_axis, neu_axis=neu_axis, *df_objs, **key_dfs)
        
    def lp(self, low=0, up=0.01, sense='max', fac_dic=None, fac_pcted=True):
        if sense == 'max':
            sense = -1
        elif sense == 'min':
            sense = 1
        lp_obj = self._obj
        lst = []
        for i, j in lp_obj.iterrows():
            fac_dic_obj = {}
            for key, value in fac_dic.items():
                if len(value) == 2:
                    fac_dic_obj[key] = [value[0].loc[i], value[1].loc[i]]
                elif len(value) == 3:
                    fac_dic_obj[key] = [value[0].loc[i], value[1], value[2]]
            obj = _lp(j, low, up, sense, fac_dic_obj, fac_pcted, False)
            lst.append(obj)
        weight = pd.concat(lst, axis=1).T
        weight.index.names = lp_obj.index.names
        weight.columns.names = lp_obj.columns.names
        limit = {i:j[1:] for i,j in fac_dic.items()}
        expose = pd.concat({i: (j[0] * weight).sum(axis=1, min_count=1) for i,j in fac_dic.items()}, axis=1).reindex(lp_obj.index)
        expose.index.names = lp_obj.index.names
        obj = type('lp_result', (), {'weight': weight, 'low':low, 'up':up, 'limit':limit, 'expose':expose})
        return obj
        
            
        
        
        
        
        
        
            
        
        
        
