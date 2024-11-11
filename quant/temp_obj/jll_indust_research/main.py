# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:45:17 2022

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
import __pandas
import flow
import __data__
import jqdatasdk as jq


finance_keys = ['tot_assets', 'tot_profit', 'tot_oper_rev']
values = {j: pd.concat([flow.stock('tot_assets', end=i, shift=2).iloc[-1].to_frame(i) for i in flow.trade_days()[252*2:]], axis=1).T for j in finance_keys}
values['returns'] = flow.stock('s_dq_pctchange')
values['market_equity'] = flow.stock('s_dq_mv')
values = pd.concat(values, axis=1)


group_keys = ['S_JQL1_CODE', 'S_JQL2_CODE', 'S_SWL1_CODE', 'S_SWL2_CODE', 'S_SWL3_CODE']
group_code = flow.stock(group_keys)

df = pd.concat([group_code, values], axis=1).stack()
df.index.names = ['TRADE_DT', 'S_INFO_WINDCODE']
df = df.set_index(group_keys, append=True)

# momentum
momentum = {i: (df['returns'] * np.log(df['market_equity'])).groupby(['TRADE_DT', i]).sum() / np.log(df['market_equity']).groupby(['TRADE_DT', i]).sum() for i in group_keys}
momentum = {i:j.unstack().rolling(126).mean().shift(21) for i,j in momentum.items()}

# top rank
top_rank = {i:df.loc[:, ~df.columns.str.contains('returns')].groupby(['TRADE_DT', i]).rank(ascending=False) for i in group_keys}
for i,j in top_rank.items():
    j = j[j.index.get_level_values(i).notnull()]
    j.index = j.index.droplevel([key for key in group_keys if key != i])
    top_rank[i] = j.unstack([2,1]).sort_index().sort_index(axis=1, level=[1,2, 0])
    
 # chinese replace
indust_keys = ['sw_l1', 'sw_l2', 'sw_l3', 'jq_l1', 'jq_l2']
indust_code = {'S_' + (''.join(i.split('_'))).upper() + '_CODE':jq.get_industries(i).iloc[:,0] for i in indust_keys}
for i,j in indust_code.items():
    j.index = pd.to_numeric(j.index, errors='ignore')
    indust_code[i] = j.to_dict()
    
for i,j in top_rank.items():
    top_rank[i] = j.rename(indust_code[i], axis=1, level=1)
    
for i,j in momentum.items():
    momentum[i] = j.rename(indust_code[i], axis=1)
    
#top_rank = {i:j[j <= 5].dropna(how='all', axis=1) for i,j in top_rank.items()}     

 



























