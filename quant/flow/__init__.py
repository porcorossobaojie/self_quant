# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 14:23:57 2021

@author: Porco Rosso
"""
import pandas as pd
import __pandas

from flow.__groups.main import stock as __Stock__
from flow.__groups.main import index as __Index__

__begin__ = '2014-01-01'
__end__ = None

stock = __Stock__(__begin__, __end__)
index = __Index__(__begin__, __end__)

def initialize(__begin__, __end__=None):
    global stock
    stock = __Stock__(__begin__, __end__)
    global index
    index = __Index__(__begin__, __end__)
    global begin
    begin = __begin__
    global end
    end = __end__

class be_list():
    def __new__(cls, limit=0):
        if not hasattr(cls, '_obj'):
            df = pd.SQL.read('join_data', 'asharedescription', ['S_INFO_WINDCODE', 'S_INFO_LISTDATE', 'S_INFO_DELISTDATE'])
            lst = []
            for i, j in df.iterrows():
                obj = pd.date_range(j['S_INFO_LISTDATE'], j['S_INFO_DELISTDATE'])
                obj = pd.Series(range(len(obj)), index=obj, name=j['S_INFO_WINDCODE'])
                lst.append(obj)
            lst = pd.concat(lst, axis=1)
            lst = lst.loc['2005-01-01':]
            lst.index = lst.index + pd.Timedelta(15, 'h')
            setattr(cls, '_obj', lst)
        df = cls._obj
        df = df.reindex(trade_days())
        df = (df >= limit).dropna(how='all', axis=1)
        return df
    
class is_st():
    def __new__(cls):
        if not hasattr(cls, '_obj'):
            st = pd.SQL.read('join_data', 'asharestatus', ['TRADE_DT', 'S_INFO_WINDCODE', 'S_DQ_ST'])
            st = st.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).iloc[:, 0].unstack()
            st = st.reindex(pd.date_range(st.index.min(), pd.Timestamp.today())).fillna(method='ffill').loc['2005-01-01':]
            setattr(cls, '_obj', st)
        df = cls._obj
        df = df.reindex(trade_days())
        df = df.dropna(how='all', axis=1)
        return df
    
class index_member():
    def __new__(cls, index_name=None, code=True, weight=True):
        if not hasattr(cls, '_obj'):
            df = pd.SQL.read('join_data', 'aindexhs300freeweight', ['ANN_DT', 'S_INFO_WINDCODE', 'S_INFO_INDCODE', 'S_DQ_WEIGHT'])
            df = df.set_index(['ANN_DT', 'S_INFO_WINDCODE']).unstack()
            df = df.tools.fillna(pd.date_range(df.index[0], pd.Timestamp.today()))
            df = df.stack()
            setattr(cls, '_obj', df)
        df = cls._obj
        df = df[df['S_INFO_INDCODE'] == index_name] if index_name is not None else df
        keys = pd.Index(['S_INFO_INDCODE', 'S_DQ_WEIGHT'])[[code, weight]]
        df = df[keys[0] if len(keys) == 1 else keys]
        df = df.unstack().astype('float64', errors='ignore')
        df = df.reindex(trade_days()).dropna(how='all', axis=1)
        return df
            
class trade_days():
    def __new__(cls):
        if not hasattr(cls, '_obj'):
            cls._obj = index('s_dq_pctchange').index
        df = cls._obj
        return df

class help():
    def __new__(cls, key):
        x = pd.concat([(i.str.contains(key) | i.str.contains(key.upper())) for j, i in stock._help.items()], axis=1).any(axis=1)
        return stock._help[x]
    
class stock_finance():
    def __new__(cls, key, shift=0, periods=1, quarter=False, Q1=3, diff=1, lt=True):
        key = key.upper()
        stock(key)
        x = stock._help[stock._help.COLUMN_NAME == key].iloc[0]
        x = getattr(stock, x.TABLE_NAME).values[key].copy()
        x = x.unstack([2,1])
        x = x.reindex(pd.date_range(trade_days()[0], trade_days()[-1])).fillna(method='ffill').stack(1)
        df = x[x.index.get_level_values(0) > x.index.get_level_values(1)]
        if lt:
            try:
                key_lt = key + '_LT'
                stock(key_lt)
                x = stock._help[stock._help.COLUMN_NAME == key_lt].iloc[0]
                x = getattr(stock, x.TABLE_NAME).values[key_lt].copy()
                x = x.unstack([2,1])
                x = x.reindex(pd.date_range(trade_days()[0], trade_days()[-1])).fillna(method='ffill')
                df = df.unstack().fillna(x).stack(1)
            except:
                pass
        df = df[df.index.get_level_values(0).isin(trade_days())]
        df.index.names = [trade_days().name, df.index.names[1]]
            
        if quarter:
            tmp = df[(df.index.get_level_values(1).month == Q1)]
            df = df.groupby(df.index.names[0]).diff(diff)
            df.loc[tmp.index] = tmp
            
        def fun(df):
            df = df.iloc[(-1* (periods + shift)):]
            df.index = range(periods + 1 + shift - df.shape[0], periods + 1 + shift) 
            return df
        obj = df.groupby(level=0).apply(lambda x: fun(x))
        obj = obj.unstack().stack(0)
        
        bools = obj.iloc[:, -1].isnull()
        while shift and bools.any():
            shift -= 1
            obj.loc[bools] =  obj.loc[bools].shift(axis=1)
            bools = obj.iloc[:, -1].isnull()
        obj = obj.iloc[:, -periods:]
        obj.columns = range(1, obj.shape[1] + 1)
        if obj.shape[1] == 1:
            obj = obj.iloc[:, 0].unstack().sort_index(axis=1)
        else:
            obj.columns.name = 'PERIODS'
            obj = obj.unstack().stack(0).sort_index(axis=1)
        obj = obj.reindex(stock(key).columns, axis=1)
        return obj

class group():
    def __new__(cls, group, func, as_df=True, **dfs):
        group_df = stock(group) if isinstance(group, str) else group
        group =  group.upper() if isinstance(group, str) else 0
            
        dfs[group] = group_df
        obj = pd.concat(dfs, axis=1).stack()
        obj.index.names = ['TEMP_%s' %(i)  if j is None else i for i,j in enumerate(obj.index.names)]
        if as_df:
            obj = obj.groupby([obj.index.names[0], group]).transform(func)
        else:
            obj = obj.groupby([obj.index.names[0], group]).apply(func)
        if len(obj.columns) < 2:
            obj = obj.iloc[:, 0].unstack()
        return obj
        
        
class post():
    def __new__(cls, price=None, shift=1):
        if not hasattr(cls, '_obj'):
            df = pd.SQL.read('join_data', 'asharedividend', ['EX_DT', 'DVD_PAYOUT_DT', 'S_INFO_WINDCODE', 'S_DIV_CASH', 'S_DIV_TOTAL'])
            df['TRADE_DT'] = df['EX_DT'].fillna(df['DVD_PAYOUT_DT'])
            df = df.groupby(['TRADE_DT', 'S_INFO_WINDCODE'])[[ 'S_DIV_CASH', 'S_DIV_TOTAL']].sum()
            df['S_DIV_TOTAL'] = 10 / (10  + df['S_DIV_TOTAL'])
            df = df.unstack()
            df = df.reindex(trade_days()[trade_days()>= df.index[0]])
            df = df.fillna(method='bfill').dropna(how='all', axis=1)
            setattr(cls, '_obj', df)
        df = cls._obj
        if price is None:
            return df
        else:
            df = df.shift(shift * -1)
            obj = (price - df['S_DIV_CASH'].reindex_like(price).fillna(0)) * df['S_DIV_TOTAL'].reindex_like(price).fillna(1)
            return obj

class hold_desc():
    def __new__(cls, price_df, post_adj, amount, turnover):
        pass


