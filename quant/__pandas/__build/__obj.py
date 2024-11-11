# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:12:04 2019

@author: Porco Rosso
"""

import numpy as np
import pandas as pd

from __pandas.__tools.__obj import _fillna
from __pandas.__build.config import __obj as config

def _group(df, rule, pct=True, order=False, axis=1, nlevels=None):
    if isinstance(rule, dict):
        # cause unkowing rule keys' level names, get rule keys' position in index / columns first.
        # split keys' position by whether stacked later or not, they are stacks, keys.
        df.index.names = [i if i is not None else 'level_i' + str(j) for j,i in enumerate(df.index.names)]
        df.columns.names = [i if i is not None else 'level_c' + str(j) for j,i in enumerate(df.columns.names)]
        nlevels = 0 if nlevels is None else nlevels
        nlevels = [nlevels] if not hasattr(nlevels, '__iter__') or isinstance(nlevels, str) else nlevels
        all_keys = list((df.columns if axis else df.index).names)
        keys = []
        stacks = []
        [keys.append(j) if j in nlevels or i in nlevels else stacks.append(j) for i, j in enumerate(all_keys)]
        x = df.stack(stacks) if axis else df.unstack(stacks).T
        x = x.reindex(rule.keys(), axis=1)
        used_keys = []
        for i in x.columns:
            x[i] = x.groupby((df.index.names if axis else stacks) + (used_keys if order else []))[i].rank(pct=True) if pct else x[i]
            x[i] = pd.cut(x[i], rule[i], labels=[i + str([rule[i][j], rule[i][j+1]]) for j in range(len(rule[i]) - 1)])
            used_keys.append(i)
        x = x.iloc[:, 0].str.cat(x.iloc[:, 1:])
        x = x.unstack(list(range(x.index.nlevels - len(stacks), x.index.nlevels)))
        x = x if axis else x.T
        return x
    else:
        x = df.rank(axis=1, pct=True) if pct else df
        n_col = x.columns.nlevels
        x = x.stack(list(range(n_col)))
        x = pd.cut(x, rule, labels=[str([rule[i], rule[i+1]]) for i in range(len(rule) - 1)])
        x = x.unstack(list(range(x.index.nlevels - n_col, x.index.nlevels)))
        return x
    
def _group_(df, rule, pct=True, order=False, nlevels=None):
    if isinstance(rule, dict):
        df.index.names = [i if i is not None else 'level_i' + str(j) for j,i in enumerate(df.index.names)]
        df.columns.names = [i if i is not None else 'level_c' + str(j) for j,i in enumerate(df.columns.names)]
        ind_keys = list(df.index.names)
        col_nlevels = [0] if nlevels is None else nlevels
        col_nlevels = [i if isinstance(i, int) else df.columns.name.index(i) for i in col_nlevels]
        df = df.stack(sorted(set(range(df.columns.nlevels)) - set(col_nlevels)))
        df = df.loc[:, list(rule.keys())]
        used_keys = []
        for k, i in enumerate(df.columns):
            df[i] = df.groupby(ind_keys + used_keys)[i].rank(pct=pct)
            df[i] = pd.cut(df[i], rule[i], labels=[str([rule[i][j], rule[i][j+1]]) for j in range(len(rule[i]) - 1)])
            if order:
                used_keys.append(i)
        df = df.unstack(list(range(df.index.nlevels)[-1 * len(col_nlevels):]))
    else:
        df = df.rank(axis=1, pct=pct)
        col_nlevels = df.columns.nlevels
        df = df.stack(list(range(col_nlevels)))
        df = pd.cut(df, rule, labels=[str([rule[i], rule[i+1]]) for i in range(len(rule) - 1)])
        df = df.unstack(list(range(df.index.nlevels)[-1 * col_nlevels:]))
    return df
                
def _weight(df, w_df=None, fillna=True, pct=True, axis=None):
    if not isinstance(df, pd.DataFrame) or not isinstance(w_df, (pd.DataFrame, type(None))) or not isinstance(fillna, bool) or not isinstance(pct, bool) or axis not in (None, 0, 1):
        raise TypeError('parameters type error.')
    axis = 0 if axis is None else axis
    if w_df is not None:
        if fillna == True:
            w_df = _fillna(w_df, df.index) if axis == 1  else _fillna(w_df, df.columns, axis=1)
        w_df = w_df.reindex_like(df)
        w_df[df.isnull()] = pd.NA
        if pct == True:
            w_df = (w_df.T / w_df.sum(axis=1)).T if axis == 1 else w_df / w_df.sum()
        return df * w_df
    else:
        if pct == True:
            x = df / df.notnull().sum() if axis == 0 else (df.T / df.notnull().sum(axis=1)).T
        else:
            x = df
        return x

def __portfolio(df_obj, returns, weight=None, shift=1, roll=1, fillna=False):
    '''
    unused
    '''
    returns = returns.rolling(roll).mean().shift((roll - 1 + shift) * -1)
    df_obj = (_fillna(df_obj, returns.index) if fillna else df_obj).reindex_like(returns)
    keys = pd.Series(list(set(df_obj.values[~df_obj.isnull()]))).dropna().sort_values().values
    if weight is not None:
        weight = (_fillna(weight, returns.index) if fillna else weight).reindex_like(returns)
        weight = weight[df_obj.notnull() & returns.notnull()].values
        w = [np.where(df_obj.values == i, weight, np.nan) for i in keys]
        w = np.nansum(np.array([i / np.nansum(i, axis=1)[:, np.newaxis] for i in w]), axis=0)
        returns *= w
        obj = {i:np.nansum(np.where(df_obj.values == i, returns, np.nan), axis=1) for i in keys}
    else:
        obj = {i:np.nanmean(np.where(df_obj.values == i, returns, np.nan), axis=1) for i in keys}
    obj = pd.DataFrame(obj, index=returns.index).replace(0, np.nan)
    return obj

def _portfolio(df_obj, returns, weight=None, shift=1, roll=1, fillna=False):
    returns = returns.rolling(roll).mean().shift((roll - 1 + shift) * -1)
    df_obj = (_fillna(df_obj, returns.index) if fillna else df_obj)
    df_obj.columns = pd.MultiIndex.from_product([['__factor__'], df_obj.columns], names=('VALUE', df_obj.columns.name)) if df_obj.columns.nlevels == 1 else df_obj.columns
    if weight is not None:
        weight = (_fillna(weight, returns.index) if fillna else weight).reindex_like(returns)
        weight = weight[returns.notnull()]
        df = pd.concat({'__returns__':returns, '__weight__':weight}, axis=1)
    else:
        df = pd.concat({'__returns__':returns}, axis=1)
    df = pd.concat([df, df_obj], axis=1).stack()
    df.index.names = [i if i is not None else 'level_i' + str(j) for j,i in enumerate(df.index.names)]
    group_keys = [df.index.names[0]] + list(df_obj.columns.get_level_values(0).unique())
    df.index = df.index.droplevel(-1)
    df = df.set_index(group_keys[1:], append=True)
    df = df.sort_index()
    if weight is not None:
        df['__returns__'] = df['__returns__'] * df['__weight__']
        obj = df.groupby(group_keys)
        obj = obj['__returns__'].sum(min_count=1) / obj['__weight__'].sum(min_count=1)
    else:
        obj = df.groupby(group_keys).mean()
    obj = obj.unstack(list(range(1, obj.index.nlevels)))
    obj.columns = obj.columns.droplevel(0) if len(obj.columns.get_level_values(0).unique()) ==1 else obj.columns
    obj = obj.astype('float64')
    return obj

def _cut(df_obj, left, right, rng_left, rng_right, pct=True, ascending=False):
    role = right - left
    lst = []
    rank = df_obj.rank(axis=1, pct=pct, ascending=ascending)
    j = rank.iloc[0]
    j = (j >= left) & (j <= right)
    lst.append(j.values)
    for i, j in rank.iloc[1:].iterrows():
        hold = (j >= left - rng_left) & (j <= right + rng_right) & lst[-1]
        lens = int(role * j.notnull().sum()) if pct else role
        updates = lens - hold.sum()
        if updates > 0:
            j = j[(~hold) & (j >= left)].sort_values().head(updates)
            hold[j.index] = True
        elif updates < 0:
            hold[~hold.index.isin(j[hold].sort_values().head(lens).index)] = False
        lst.append(hold.values)
    lst = pd.DataFrame(np.vstack(lst), index=df_obj.index, columns=df_obj.columns)
    return lst

def _event(df_obj, limit):
    df_obj = df_obj.notnull().astype(float).replace(0, np.nan)
    for i in range(1, limit):
        df_obj[df_obj.isnull() & df_obj.shift().notnull()] = i + 1
    return df_obj

def _trend(df_obj, periods, how):
    dic = {}
    if len(df_obj) >= periods:
        for i in range(periods, len(df_obj) + 1):
            df = df_obj.iloc[i-periods : i]
            df.index = pd.RangeIndex(periods)
            dic[df_obj.index[i-1]] = df
        dic = pd.concat(dic, axis=1).T
        dic.index.names = list(df_obj.index.names) + list(df_obj.columns.names)
        if how == 'head':
            dic = dic.sub(dic.iloc[:, 0], axis=0)
        elif how == 'btm':
            dic = dic.sub(dic.iloc[:, -1], axis=0)
        elif how == 'mean':
            dic = dic.sub(dic.mean(axis=1), axis=0)
        elif how == 'trend':
            dic = dic.sub(dic.iloc[:, 0], axis=0)
            df = dic.iloc[:, -1] / (periods - 1)
            df = np.repeat(df.values, periods - 1).reshape(-1, periods-1).cumsum(axis=1)
            dic.iloc[:, 1:] =  dic.iloc[:, 1:].sub(df, axis=0)
        elif how == 'roll_mean':
            df = df_obj.rolling(periods, min_count=1).mean()
            df = pd.concat({i:df.shift(i) for i in range(periods)}, axis=1).stack()
            dic = dic - df.reindex_like(dic)
        return dic
    else:
        raise ValueError('length of DataFrame is smaller than periods')
    
@pd.api.extensions.register_dataframe_accessor(config.pandasAttrName)
class build():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        
    def group(self, rule=None, pct=True, order=False, nlevels=None, multi_index=False):
        '''
        ------------
        
        Explain:
            group dataframe's values by parameters.
        
        ------------
        
        Parameters:
        
            sortDict:
                dict, list.
                if parameter sortDict is given such as {factor_name_1:[0,0.5,1], factor_name_2:[0,0.3,0.8,1]......},
                if parameter sortDict is given such as [0,0.6,0.8,1], func will group dataframe by list information.
            
            pct:
                bool.
                whether mapping dataframe's values into (0 ~ 1).
            
            order:
                bool.
                whether group factors ordered from rule or not which lets every sub group in same size.
            
            axis:
                int,
                {0, 1}, recommand 0.
                the axis keys on.
                
            nlevels:
                int,
                recommand 0.
                the levels keys on.
        
        ------------
        
        Returns:
            dataframe.
        
        ------------
        '''
        rule = np.linspace(0,1,11).round(2) if rule is None else rule
        if multi_index:
            return _group_(self._obj, rule=rule, pct=pct, order=order, nlevels=nlevels)
        else:
            return _group(self._obj, rule=rule, pct=pct, order=order, nlevels=nlevels)
    
    def weight(self, w_df=None, fillna=True, pct=True, axis=None):
        '''
        ------------
        
        Explain:
            weighted dataframe by w_df.
        
        ------------
        
        Parameters:
        
            w_df:
                dataframe, None.
                using for weighted dataframe.
                if is None, return dataframe self.
            
            fillna:
                bool.
                whether _fillna w_df by dataframe's index/columns according to parameter axis, 
                if axis = 1, fillna on axis 0; if axis = 0 ,fillna on axis 1.
            
            pct:
                bool.
                whether mapping w_df.values by axis in Sum = 1.
            
            axis:
                {0, 1}, recommand 0.
                the row not fillna, the row pcted.
        
        ------------
        
        Returns:
            dataframe.
        
        ------------
        '''
        return _weight(self._obj, w_df=w_df, fillna=fillna, pct=pct, axis=axis)
    
    def portfolio(self, returns, weight=None, shift=1, roll=1, fillna=True):
        '''
        ------------
        
        Explain:
            get portfolio returns by group information(dataframe self), returns, weight and other parameters.
        
        ------------
        
        Parameters:
        
            returns:
                dataframe.
                the returns of stocks.
            
            weight:
                dataframe.
                the hold pct of each stock in total portfolio.
            
            shift:
                int.
                the day delayed from get group informaton to change portfolio.
            
            roll:
                int.
                calculate rolling mean as returns.
            
            fillna:
                bool.
                whether fill self like returns.
        
        ------------
        
        Returns:
            dataframe.
        
        ------------
        '''
        return _portfolio(self._obj, returns=returns, weight=weight, shift=shift, roll=roll, fillna=fillna)
    
    def cut(self, right, rng_right=0, left=0, rng_left=0, pct=True, ascending=False):
        '''
        ------------
        
        Explain:
            get bool dataframe selected by value information(dataframe self), left, right rng_left, rng_right and other parameters.
            
        ------------
        
        Parameters:
            
            right:
                int, float.
                the right limit of dataframe's values.
                
            rng_right:
                int, float.
                the range whether selecting when stocks had been selected at t-1 if out of right or not.
                
            left:
                int, float.
                the left limit of dataframe's values.
                
            rng_right:
                int, float.
                the range whether selecting when stocks had been selected at t-1 if out of left or not.
                
            pct:
                bool.
                right, rng_right, left, rng_left will be regard as percent if True else absulate value.
                
            ascending:
                bool.
                sort values by ascending or not.
                
        ------------
        
        Returns:
            dataframe.
            
        ------------
        '''
        return _cut(self._obj, left, right, rng_left, rng_right, pct, ascending)
    
    def event(self, limit=44):
        return _event(self._obj, limit)
    
    def trend(self, periods, how=None):
        return _trend(self._obj, periods, how)
        
    









