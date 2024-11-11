# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 09:25:09 2022

@author: Porco Rosso
"""

import flow
import __capital__
from __factors__ import meta, barra, finance, trade
import pandas as pd
import numpy as np

meta.initialize()
returns = trade.stock('s_dq_pctchange')
turnover = returns.rolling(21, min_periods=10).mean()
beta = barra.BETA()
liq = barra.LIQUIDITY()
earn = barra.EARNING_YEILD()

neu_dict = {'me':barra.SIZE(), 'bm':barra.BOOK_TO_PRICE(), 'non':barra.NON_LINEAR_SIZE(),  'mom':barra.MOMENTUM(), 'beta':beta, 'earn':earn}
group_dict = pd.concat({i:neu_dict[i] for i in ['me', 'bm', 'mom', 'beta']}, axis=1)
grouo_dict = group_dict.build.group({'me':[0, 0.5, 1], 'bm':[0, 0.5, 1], 'mom':[0, 0.5, 1], 'beta':[0, 0.5, 1]}, order=True)
if300 = flow.index_member('399300.SZ', False)
ic500 = flow.index_member('000905.SH', False)


revenue = {'TOT_OPER_REV_TTM':finance.TOT_OPER_REV_TTM(), 'OPER_REV_TTM':finance.OPER_REV_TTM()}
profit = {'TOT_PROFIT_TTM':finance.TOT_PROFIT_TTM(), 'OPER_PROFIT_TTM': finance.OPER_PROFIT_TTM(), 'EBIT':finance.EBIT(), 'NET_PROFIT_TTM':finance.NET_PROFIT_TTM(), 'PAR_COMP_NET_INC_TTM':finance.PAR_COMP_NET_INC_TTM()}
growth = {'OPER_REV_GROWTH_RATIO': finance.OPER_REV_GROWTH_RATIO(), 'OPER_PROFIT_GROWTH_RATIO': finance.OPER_PROFIT_GROWTH_RATIO(), 'TOT_ASSET_GROWTH_RATIO':finance.TOT_ASSET_GROWTH_RATIO(), 'OPER_CASH_GROWTH_RATIO':finance.OPER_CASH_GROWTH_RATIO()}
equity = {'ROA_TTM':finance.ROA_TTM(), 'ROE_TTM':finance.ROE_TTM()}
cash = {'NET_OPER_CASH_TTM': finance.NET_OPER_CASH_TTM(), 'IM_NET_CASH_FLOWS_OPER_ACT': finance.IM_NET_CASH_FLOWS_OPER_ACT()}
assets = {'TOT_ASSETS':finance.TOT_ASSETS(), 'NET_ASSETS':finance.NET_ASSETS()}

rev = {i:j.values.stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid for i,j in revenue.items()}
rev = pd.concat(rev, axis=1).stack().mean(axis=1).unstack()

pro = {i:j.values.stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid for i,j in profit.items()}
pro = pd.concat(pro, axis=1).stack().mean(axis=1).unstack()

equ = {i:j.values.stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid for i,j in equity.items()}
equ = pd.concat(equ, axis=1).stack().mean(axis=1).unstack()

grow = {i:j.values.stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid for i,j in growth.items()}
grow = pd.concat(grow, axis=1).stack().mean(axis=1).unstack()

cas = {i:j.values.stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid for i,j in cash.items()}
cas = pd.concat(cas, axis=1).stack().mean(axis=1).unstack()

ass = {i:j.values.stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid for i,j in assets.items()}
ass = pd.concat(ass, axis=1).stack().mean(axis=1).unstack()

liq = barra.LIQUIDITY().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1

resid = barra.RESIDUAL_VOLATILITY().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1

tech_01 = trade.TURNOVER_Z().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid
tech_02 = trade.DEVIATION_CORR_TURNOVER().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1
tech_03 = trade.OPEN_ABNORMAL().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1
tech_04 = trade.VOLUME_AVG().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1
tech_05 = trade.VOLUME_HIGH().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1
tech_06 = trade.DAY_STD().stats.standard(axis=1).stats.neutral(neu_axis=1, **neu_dict).resid * -1

facs = pd.concat({'group':grouo_dict, 'revenue':rev, 'profit':pro, 'growth':grow, 'cash':cas, 'assets':ass, 'equity':equ, 'liq':liq, 'resid':resid, '01':tech_01, '02':tech_02, '03':tech_03, '04':tech_04, '05':tech_05}, axis=1)
facs = facs.stack()
facs = facs.groupby(['TRADE_DT', 'group'])[facs.columns.drop('group')].rank(pct=True)
g1 = facs.fillna(0.5).sum(axis=1).unstack()
g2 = g1.build.cut(20, 50, pct=False)
g3 = pd._DataFrame(g2).shift().loc['2017-01-01':].chain()

'''
ifs = g1.reindex_like(if300)[if300.notnull()].build.cut(30, 60, pct=False)
ics = g1.reindex_like(ic500)[ic500.notnull()].build.cut(50, 100, pct=False)
alls = g2
x1 = pd.concat({'ifs':ifs, 'ics':ics, 'all':alls}, axis=1).stack().sum(axis=1).replace(0, np.nan).unstack()
x2 = pd._DataFrame(ics).shift().loc['2017-01-01':].chain()
'''







