# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 11:37:40 2023

@author: admin
"""

import flow
import __pandas
import pandas as pd
import numpy as np

begin = '2018'
indust = flow.stock('s_jql2_code').loc[begin:]
cols = (['TOT_OPER_REV_TTM', 'OPER_REV_TTM', 
            'TOT_PROFIT_TTM', 'OPER_PROFIT_TTM', 'EBIT', 'NET_PROFIT_TTM', 
            'OPER_REV_GROWTH_RATIO', 'OPER_PROFIT_GROWTH_RATIO', 'TOT_ASSET_GROWTH_RATIO', 'OPER_CASH_GROWTH_RATIO', 
            'ROA_TTM', 'ROE_TTM',
            'NET_OPER_CASH_TTM', ])

flow.stock(cols)
mv = flow.stock('s_val_mv')
returns = flow.stock('s_dq_pctchange')
price = np.log(flow.stock('s_dq_close'))

dic = {}
for i,j in indust.iterrows():
    dic[i] = pd.concat([returns.loc[i], j.stats.const()], axis=1).stats.OLS(const=True).params[1:]
dic = pd.concat(dic, axis=1).T
dic = dic.rolling(126, min_periods=1).mean()
indust_factor = dic.copy()
indust = indust.stack().reset_index()
indust['TRADE_DT'] = indust['TRADE_DT'].apply(lambda x: str(x))
dic = dic.stack().reset_index()
dic.columns = ['TRADE_DT', 0, 'prem']
dic['TRADE_DT'] = dic['TRADE_DT'].apply(lambda x: str(x))
prem = pd.merge(indust, dic, on=['TRADE_DT', 0], how='left')
prem['TRADE_DT'] = pd.to_datetime(prem['TRADE_DT'])
prem = prem.set_index(['TRADE_DT', 'S_INFO_WINDCODE'])['prem'].unstack()

dic = {}
for i in cols:
    fac = flow.stock(i) / mv / 10e6
    resid = price.stats.neutral(neu_axis=1, fac=fac).params
    fac = fac.mul(resid.iloc[:, 1].rolling(42, min_periods=1).mean(), axis=0)
    dic[i] = fac
dic['prem'] = prem

test1 = price.stats.neutral(neu_axis=1, **dic)



