# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:31:59 2024

@author: admin
"""

import pandas as pd
import __pandas
import numpy as np
import flow

mint_index = pd.SQL.read('join_data', 'aindexeodprices1min').iloc[:, 1:].set_index(['TRADE_DT', 'S_INFO_WINDCODE'])
mint_index['date'] = mint_index.index.get_level_values('TRADE_DT').date
index = flow.index('s_dq_pctchange')
index_amount = flow.index('s_dq_volume')
index_rank = index_amount.rolling(252).rank()
keys = ['corr', 'mean', 'z1', 'z2']

def fac(after):

    after_corr = after.groupby(['date', 'S_INFO_WINDCODE']).apply(lambda x: x['S_DQ_PCTCHANGE'].corr(x['S_DQ_VOLUME']))
    after_mean = after.groupby(['date', 'S_INFO_WINDCODE']).mean()['S_DQ_PCTCHANGE']
    after_std = after.groupby(['date', 'S_INFO_WINDCODE']).std()['S_DQ_PCTCHANGE']
    after_z1 =  (after.groupby(['date', 'S_INFO_WINDCODE']).mean() / after.groupby(['date', 'S_INFO_WINDCODE']).std())['S_DQ_PCTCHANGE']
    after_z2 =  (after.groupby(['date', 'S_INFO_WINDCODE']).mean() / mint_index.groupby(['date', 'S_INFO_WINDCODE']).std())['S_DQ_PCTCHANGE']
    after_fac = pd.concat({'corr':after_corr, 'mean': after_mean, 'z1':after_z1, 'z2':after_z2, 'std':after_std}, axis=1)
    after_fac = after_fac.unstack()
    after_fac.index = pd.to_datetime(after_fac.index) + pd.Timedelta(15, 'h')
    
    return after_fac

def long_short(df):
    f1 = df[df.sub(df.min(axis=1), axis=0) == 0]
    short = index.reindex_like(f1)[f1.shift().notnull()].sum(axis=1)
    f2 = df[df.sub(df.max(axis=1), axis=0) == 0]
    long = index.reindex_like(f2)[f2.shift().notnull()].sum(axis=1)
    return (long - short)

def l_s(df):
    ind_rank = index_rank.reindex_like(df)
    f1 = df[ind_rank.sub(ind_rank.max(axis=1), axis=0) != 0]
    f1 = f1[f1.sub(f1.min(axis=1), axis=0) == 0]
    short = index.reindex_like(f1)[f1.shift().notnull()].sum(axis=1)
    f2 = df[ind_rank.sub(ind_rank.min(axis=1), axis=0) != 0]
    f2 = f2[f2.sub(df.max(axis=1), axis=0) == 0]
    long = index.reindex_like(f2)[f2.shift().notnull()].sum(axis=1)
    return (long - short)
    
    

g1 = fac(mint_index)
total = pd.concat({i:g1['z1'].rolling(i).mean() for i in range(5,21)}, axis=1).stack().mean(axis=1).unstack()
index_z = pd.concat({i:index.rolling(i).mean() / index.rolling(i).std() for i in range(10, 21)}, axis=1).stack().mean(axis=1).unstack()

after = mint_index[(mint_index.index.get_level_values('TRADE_DT').hour < 9)
                   | (mint_index.index.get_level_values('TRADE_DT').hour >= 13) & (mint_index.index.get_level_values('TRADE_DT').minute > 0)]

g2 = fac(after)
to_30min = pd.concat({i:g2['z2'].rolling(i).mean() for i in range(1,3)}, axis=1).stack().mean(axis=1).unstack()

















