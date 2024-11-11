# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 15:33:36 2022

@author: Porco Rosso
"""

import numpy as np

def ts_rank_unit(array_obj, cut, pct, func, **kwargs):
    x = (array_obj <= array_obj[-1]).sum(axis=0)
    nans = (~np.isnan(array_obj)).sum(axis=0)
    x = np.where(nans == 0, np.nan, x)
    if pct:
        x = x / nans
    return x

def ts_sort_unit(array_obj, cut, pct, func, **kwargs):
    endwith = True if cut > 0 else False
    x = np.ma.sort(array_obj, axis=0, endwith=endwith)
    x = x[:cut] if endwith else x[cut:]
    x = func(x, axis=0, **kwargs) if func is not None else x
    return x
    
def ts_argsort_unit(array_obj, cut, pct, func, **kwargs):
    endwith = True if cut > 0 else False
    x = np.ma.array(np.ma.argsort(array_obj, axis=0, endwith=endwith), mask=(np.sort(array_obj.mask, axis=0) if endwith else np.sort(array_obj.mask, axis=0)[::-1]))
    x = x[:cut] if endwith else x[cut:]
    x = func(x, axis=0, **kwargs) if func is not None else x
    return x
    
    










