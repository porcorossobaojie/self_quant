# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 10:59:37 2021

@author: Porco Rosso
"""

import flow
import __capital__
from __factors__ import meta, barra, finance, trade
import pandas as pd
import numpy as np

meta.initialize()

me = barra.SIZE()
bm = barra.BOOK_TO_PRICE()
resid = barra.RESIDUAL_VOLATILITY()
resid.index.name = 'TRADE_DT'
returns = barra.stock('s_dq_pctchange')
momentum = returns.rolling(126, min_periods=63).mean().shift(21).stats.neutral(neu_axis=1, me=me).resid
turnover = returns.rolling(21, min_periods=10).mean().stats.neutral(neu_axis=1, me=me).resid
indexs = barra.index('s_dq_pctchange')['000905.SH']
indust = barra.stock('s_jql2_code').fillna(method='bfill')

revenue = {'TOT_OPER_REV_TTM':finance.TOT_OPER_REV_TTM(), 'OPER_REV_TTM':finance.OPER_REV_TTM()}
profit = {'TOT_PROFIT_TTM':finance.TOT_PROFIT_TTM(), 'OPER_PROFIT_TTM': finance.OPER_PROFIT_TTM(), 'EBIT':finance.EBIT(), 'NET_PROFIT_TTM':finance.NET_PROFIT_TTM(), 'PAR_COMP_NET_INC_TTM':finance.PAR_COMP_NET_INC_TTM()}
growth = {'OPER_REV_GROWTH_RATIO': finance.OPER_REV_GROWTH_RATIO(), 'OPER_PROFIT_GROWTH_RATIO': finance.OPER_PROFIT_GROWTH_RATIO(), 'TOT_ASSET_GROWTH_RATIO':finance.TOT_ASSET_GROWTH_RATIO(), 'OPER_CASH_GROWTH_RATIO':finance.OPER_CASH_GROWTH_RATIO()}
equity = {'ROA_TTM':finance.ROA_TTM(), 'ROE_TTM':finance.ROE_TTM()}
cash = {'NET_OPER_CASH_TTM': finance.NET_OPER_CASH_TTM(), 'IM_NET_CASH_FLOWS_OPER_ACT': finance.IM_NET_CASH_FLOWS_OPER_ACT()}
assets = {'TOT_ASSETS':finance.TOT_ASSETS(), 'NET_ASSETS':finance.NET_ASSETS()}

ind_prem = pd.concat({'indust':indust, 'returns':returns, 'me':np.log(me).rank(axis=1,pct=True)}, axis=1).stack().groupby(['TRADE_DT', 'indust'])['returns', 'me'].mean().unstack()



profit_values = pd.concat({i:j.values.stats.standard(axis=1, rank=(-5,5)) for i,j in profit.items()}, axis=1)
profit_values = profit_values.stack().mean(axis=1).unstack()
revenue_values = pd.concat({i:j.values.stats.standard(axis=1, rank=(-5,5)) for i,j in revenue.items()}, axis=1)
revenue_values = revenue_values.stack().mean(axis=1).unstack()

growth_values = pd.concat({i:j.values.stats.standard(axis=1, rank=(-5,5)) for i,j in growth.items()}, axis=1)
growth_values = growth_values.stack().mean(axis=1).unstack()

equity_values = pd.concat({i:j.values.stats.standard(axis=1, rank=(-5,5)) for i,j in equity.items()}, axis=1)
equity_values = equity_values.stack().mean(axis=1).unstack()

cash_values = pd.concat({i:j.values.stats.standard(axis=1, rank=(-5,5)) for i,j in cash.items()}, axis=1)
cash_values = cash_values.stack().mean(axis=1).unstack()

assets_values = pd.concat({i:j.values.stats.standard(axis=1, rank=(-5,5)) for i,j in assets.items()}, axis=1)
assets_values = assets_values.stack().mean(axis=1).unstack()

g1 = pd.concat({'profit':profit_values.rank(axis=1, pct=True), 'revenue':revenue_values.rank(axis=1, pct=True), 'growth':growth_values.rank(axis=1, pct=True), 'equity':equity_values.rank(axis=1, pct=True), 'cash':cash_values.rank(axis=1, pct=True), 'asset':assets_values.rank(axis=1, pct=True)}, axis=1).stack()
g2 = g1[(g1['profit'] > 0.5) & ((g1 > 0.5).sum(axis=1) >= 4) & ((g1 <= 0.4).sum(axis=1) <= 0)].fillna(0.5).sum(axis=1).unstack()
turn = barra.stock('s_dq_freeturnover')
turn = (turn.rolling(21).mean() / turn.rolling(252).mean())
g3 = pd.concat({'fac':g2, 'turn':turn.rank(axis=1, pct=True), 'resid':resid.rank(axis=1, pct=True)}, axis=1).stack()
g4 = g3[(g3['resid'] < 0.9)]
g4 = g4['fac'].unstack()
g6 = g4[g4.build.cut(200, 220, pct=False)]
g6 = g6.dropna(how='all', axis=1)
g7 = pd._DataFrame(g6).shift().loc['2017-01-01':].chain()


'''
g1 = pd.concat({'profit':profit_values.rank(axis=1, pct=True), 'revenue':revenue_values.rank(axis=1, pct=True), 'growth':growth_values.rank(axis=1, pct=True), 'equity':equity_values.rank(axis=1, pct=True), 'cash':cash_values.rank(axis=1, pct=True), 'asset':assets_values.rank(axis=1, pct=True), 'me':me, 'resid':resid.rank(axis=1, pct=True), 'indust':indust}, axis=1).stack()
g2 = g1.copy()
g2['me'] = g2.groupby(['TRADE_DT', 'indust'])['me'].rank(pct=True)
g2['me'] = pd.cut(g2['me'], np.linspace(0,1,21).round(2))
g2[['profit', 'revenue', 'growth', 'equity', 'cash', 'asset']] = g2.groupby(['TRADE_DT', 'me'])['profit', 'revenue', 'growth', 'equity', 'cash', 'asset'].rank(pct=True)
g2 = g1[g1['profit'] > 0.0].fillna(0.5)
g2 = g2[((g2[['profit', 'revenue', 'growth', 'equity', 'cash', 'asset']] > 0.3).all(axis=1)) & (g2['resid'] < 0.9)]
g2['factor'] = g2[['profit', 'revenue', 'growth', 'equity', 'cash', 'asset']].sum(axis=1)
g4 = g2['factor'].unstack()
g6 = g4[g4.build.cut(20, 50, pct=False)].dropna(how='all', axis=1)
g7 = pd._DataFrame(g6).shift().loc['2017-01-01':].chain()
'''
'''
g1 = pd.concat({'profit':profit_values.rank(axis=1, pct=True), 'revenue':revenue_values.rank(axis=1, pct=True), 'growth':growth_values.rank(axis=1, pct=True), 'equity':equity_values.rank(axis=1, pct=True), 'cash':cash_values.rank(axis=1, pct=True), 'asset':assets_values.rank(axis=1, pct=True), 'me':me.build.group(np.linspace(0,1,11).round(2))}, axis=1).stack()
g2 = g1.groupby(['me', 'TRADE_DT']).rank(pct=True)
g2.index
g3 = g2[(g2['profit'] > 0.5) & ((g2 > 0.5).sum(axis=1) >=4)].fillna(0.5).sum(axis=1).unstack()
g3 = pd.concat({'fac':g3, 'resid':resid.rank(axis=1, pct=True)}, axis=1).stack()
g4 = g3[(g3['resid'] < 0.9)]
g4 = g4['fac'].unstack()
g6 = g4[g4.build.cut(200, 220, pct=False)]
g6 = g6.dropna(how='all', axis=1)
g7 = pd._DataFrame(g6).shift().loc['2017-01-01':].chain()
'''

