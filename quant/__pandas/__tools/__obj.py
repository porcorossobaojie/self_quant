# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:03:46 2019

@author: Porco Rosso
"""
import numpy as np
import pandas as pd
from __pandas.__tools.config import __obj as config

def __fillna(df_obj, lst):
    df_obj = df_obj.sort_index()
    x = sorted(filter(lambda i: df_obj.index[0] <= i <= lst[-1], (set(lst) | set(df_obj.index))))
    if len(x) == 1 and (x[0] in lst and x[0] not in df_obj.index):
        z = pd.DataFrame(pd.NA, index=[x[0]], columns=df_obj.columns) if isinstance(df_obj, pd.DataFrame) else pd.Series(pd.NA, index=[x[0]], name=df_obj.name)            
    else:
        keys = sorted(filter(lambda i: i <=x[-1], df_obj.index))
        keys = [x.index(i) for  i in keys]
        values = df_obj.values
        lst = [values[i].repeat(keys[i+1] - keys[i]).reshape(values.shape[-1], -1).T for i in range(len(keys)-1)]
        add = len(x) - x.index(x[keys[-1]]) 
        add = values[len(keys)-1].repeat(add).reshape(values.shape[-1], -1).T
        lst.append(add)
        lst = np.vstack(lst).reshape(len(x), -1)
        z = pd.DataFrame(lst, index=x, columns=df_obj.columns)
    z.index.names = df_obj.index.names
    return z

def _fillna(df_obj, fill_list):
    df_obj = df_obj.sort_index()
    old_idx = df_obj.index.to_list()
    index = sorted(fill_list)
    if index[-1] >= old_idx[0]:
        values = df_obj.values
        lst = []
        new_idx = sorted(set(df_obj.index) | set(index))
        position = [new_idx.index(i) for i in old_idx]
        position.append(len(new_idx))
        for i, j in enumerate(position[:-1]):
            repeat = position[i+1] - j
            array = values[i]
            array = array.repeat(repeat)
            lst.append(array.reshape(df_obj.shape[1], -1).T if repeat != 1 else array.reshape(1, -1))
        lst = np.concatenate(lst)
        lst = pd.DataFrame(lst, columns=df_obj.columns, index=new_idx[position[0]:]).reindex(index)
    else:
        lst = pd.DataFrame(np.nan, index=index, columns=df_obj.columns)
    lst.index.name = getattr(fill_list, 'name', None) if getattr(fill_list, 'name', None) is not None else df_obj.index.name
    return lst   

def _fillna_3D(df_obj, fill_list, fill_axis):
    axis = [0,1,2]
    axis_0 = df_obj.index.get_level_values(axis.pop(fill_axis)).unique()
    fill_index = sorted(set(axis_0) | set(fill_list)) if fill_list is not None else axis_0
    index, columns =(df_obj.index.get_level_values(i).unique() for i in axis)
    df = df_obj.unstack(axis[-1])
    keys = []
    lst = [np.full((len(index), len(df.columns)), np.nan)]
    for i,j in enumerate(fill_index):
        keys.append(j)
        if j not in axis_0:
            lst.append(lst[-1])
        else:
            np_obj = df.xs(j, level=fill_axis).reindex(index).values
            np_obj = np.where(np.isnan(np_obj), lst[-1], np_obj)
            lst.append(np_obj)
    lst = pd.DataFrame(np.concatenate(lst[1:]), index=pd.MultiIndex.from_product([fill_index, index], names=[df_obj.index.names[fill_axis], index.name]), columns=df.columns)
    return lst
                    
def _shift(df_obj, n):
    bools = df_obj.iloc[-1].isnull()
    while n > 0 and bools.any():
        n -= 1
        df_obj.loc[:, bools] = df_obj.loc[:, bools].shift()
        bools = df_obj.iloc[-1].isnull()
    return df_obj

@pd.api.extensions.register_dataframe_accessor(config.pandasAttrName)
class tools():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        
    def fillna(self, fill_list):
        '''
        ------------
        
        Explain:
            fill na by reindex in lst.
        
        ------------
        
        Parameters:
            fill_list:
                iterable.
                new indexs insert in dataframe for fillna.
        
        ------------
        
        Returns:
            dataframe.
            func fillna from dataframe.index[i] -> dataframe.index[i + 1] after lst insert in dataframe.
        
        ------------
        '''
        return _fillna(self._obj, fill_list)
    
    def fillna_3D(self, fill_list=None, fill_axis=0):   
        return _fillna_3D(self, fill_list, fill_axis)
    
    def shift(self, n=1):
        return _shift(self._obj, n)

@pd.api.extensions.register_series_accessor(config.pandasAttrName)
class series_stats():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def fillna_3D(self, fill_list=None, fill_axis=0):   
        return _fillna_3D(self, fill_list, fill_axis)


