# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 21:31:29 2024

@author: Porco Rosso
"""
import numpy as np
import pandas as pd
import __pandas



def _hold(history,                            # dataframe for holding futures 
          act,                             # datarfame for this period   
          unit_price,                         # price for 1 point
          min_unit,                           # min_rank for 1 point
          open_interest = 'open_interest',    # open interest column name
          money =         'money',            # money column name
          volume =        'volume',           # volume column name
          price =         'price',            # given hold future price name
          limit =         500,
          **kwargs):
    
    if act[volume] == 0:
        history.index = [act.name] * len(history)
        return history
 
    min_count = len(str(min_unit).split('.')[-1])
            
    act_price = int(act[money] / act[volume] / unit_price / min_unit) * min_unit
    else_price = int(round((act[money] - act_price * act[volume] * unit_price) / unit_price / min_unit, 0))
    dic = {act_price:act[volume] - else_price, act_price + min_unit:else_price}
    dic = pd.Series(dic).reset_index()
    dic.columns = [price, volume]

    if history is None:
        dic.index = [act.name] * len(dic)
        return dic
    else:
        history = history.copy()
        
    df = pd.concat([history, dic])
    df[price] = df[price].round(min_count)
    df = df.groupby(price)[volume].sum()
    df = df[df > 0]
        
    close = int(act[volume] - (act[open_interest] - history[volume].sum()))    
    if close:
        if close < 0:
            raise ValueError()
        df = df * (1 - close / (df.sum() if df.sum() else 1))
        
    if limit is not None and len(df) > limit:
        df = df.sort_values(ascending=False)
        temp1 = df.iloc[:limit - 1]
        temp2 = df.iloc[limit - 1:]
        sums = temp2.sum()
        temp2 = [(temp2.index * temp2).sum() / sums, sums]
        temp2[0] = round(temp2[0] / min_unit, 0) * min_unit
        if temp2[0] in temp1.index:
            temp1[temp2[0]] = temp1[temp2[0]] + temp2[1]
        else:
            temp1[temp2[0]] = temp2[1]
        df = temp1.sort_index()
    
    df = df.reset_index()    
    df.index = [act.name] * len(df)       
    return df
    
def _hold_desc(future, unit_price, min_unit, open_interest, money, volume, **kwargs):
    lst = [None]
    future = future.dropna(how='all')
    for i,j in future.iterrows():
        lst.append(_hold(lst[-1], j, unit_price, min_unit, open_interest, money, volume, **kwargs))
    lst = lst[1:]
    keys = future.index
    dic = dict(zip(keys, lst))
    return dic
        
        
        
        





























