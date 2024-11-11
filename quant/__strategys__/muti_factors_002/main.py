# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 17:58:01 2021

@author: lenovo
"""

import flow
import __capital__
from __factors__ import meta, barra, finance, trade
import pandas as pd
import numpy as np
import __data__

__data__.joinquant.daily()


flow.initialize('2019-01-01')
meta.initialize()

me = barra.SIZE()
bm = barra.BOOK_TO_PRICE()
resid = barra.RESIDUAL_VOLATILITY()
resid.index.name = 'TRADE_DT'
returns = barra.stock('s_dq_pctchange')
momentum = returns.rolling(126, min_periods=63).mean().shift(21).stats.neutral(neu_axis=1, me=me).resid
turnover = returns.rolling(21, min_periods=10).mean().stats.neutral(neu_axis=1, me=me).resid
turn = barra.stock('s_dq_freeturnover')
turn = (turn.rolling(21).mean() / turn.rolling(252).mean())
indust = barra.stock('s_jql2_code').fillna(method='bfill')

revenue = {'TOT_OPER_REV_TTM':finance.TOT_OPER_REV_TTM(), 'OPER_REV_TTM':finance.OPER_REV_TTM()}
profit = {'TOT_PROFIT_TTM':finance.TOT_PROFIT_TTM(), 'OPER_PROFIT_TTM': finance.OPER_PROFIT_TTM(), 'EBIT':finance.EBIT(), 'NET_PROFIT_TTM':finance.NET_PROFIT_TTM(), 'PAR_COMP_NET_INC_TTM':finance.PAR_COMP_NET_INC_TTM()}
growth = {'OPER_REV_GROWTH_RATIO': finance.OPER_REV_GROWTH_RATIO(), 'OPER_PROFIT_GROWTH_RATIO': finance.OPER_PROFIT_GROWTH_RATIO(), 'TOT_ASSET_GROWTH_RATIO':finance.TOT_ASSET_GROWTH_RATIO(), 'OPER_CASH_GROWTH_RATIO':finance.OPER_CASH_GROWTH_RATIO()}
equity = {'ROA_TTM':finance.ROA_TTM(), 'ROE_TTM':finance.ROE_TTM()}
cash = {'NET_OPER_CASH_TTM': finance.NET_OPER_CASH_TTM(), 'IM_NET_CASH_FLOWS_OPER_ACT': finance.IM_NET_CASH_FLOWS_OPER_ACT()}
assets = {'TOT_ASSETS':finance.TOT_ASSETS(), 'NET_ASSETS':finance.NET_ASSETS()}

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

g1 = pd.concat({'profit':profit_values.rank(axis=1, pct=True), 'revenue':revenue_values.rank(axis=1, pct=True), 'growth':growth_values.rank(axis=1, pct=True), 'equity':equity_values.rank(axis=1, pct=True), 'cash':cash_values.rank(axis=1, pct=True), 'asset':assets_values.rank(axis=1, pct=True), 'me':me, 'resid':resid.rank(axis=1, pct=True), 'indust':indust}, axis=1).stack()
g2 = g1.copy()
g2['me'] = g2.groupby(['TRADE_DT', 'indust'])['me'].rank(pct=True)
g2['me'] = pd.cut(g2['me'], np.linspace(0,1,21).round(2))
g2[['profit', 'revenue', 'growth', 'equity', 'cash', 'asset']] = g2.groupby(['TRADE_DT', 'me'])['profit', 'revenue', 'growth', 'equity', 'cash', 'asset'].rank(pct=True)
g2 = g1[g1['profit'] > 0.0].fillna(0.5)
g2 = g2[((g2[['profit', 'revenue', 'growth', 'equity', 'cash', 'asset']] > 0.3).all(axis=1)) & (g2['resid'] < 0.9)]
g2['factor'] = g2[['profit', 'revenue', 'growth', 'equity', 'cash', 'asset']].sum(axis=1)
g4 = g2['factor'].unstack()
g6 = g4[g4.build.cut(50, 50, pct=False)].dropna(how='all', axis=1)
g6.iloc[-1].dropna().to_excel('d:\\daily_report\\report%s.xlsx' %(pd.Timestamp.now().date().__str__())) 
g7 = pd._DataFrame(g6).shift().loc[pd.to_datetime('2020-07-12'):].chain()

indexs = barra.index('s_dq_pctchange')['000905.SH']
different = [j[0].different for i,j in g7.items()]
different = pd.concat([i.returns for i in different], axis=1).T
different['000905.SH'] = indexs.loc[different.index]
different['alpha'] = different['Effective_Return'] - different['000905.SH']
try:
    hold = pd.read_excel('d:\\daily_report\\hold_%s.xlsx' %(pd.Timestamp.now().date().__str__()), usecols=[1,4], dtype={0:str, 1:float}, thousands=',')
except:
    hold = (pd._Series(g6.iloc[-1].dropna()).notnull().settle.assets(2800000) / flow.stock('S_DQ_CLOSE').loc[g6.index[-1]]).dropna()
    hold = hold.round(-2)
    order = pd.DataFrame(columns = ['市场', '合约代码', '委托方向', '投机套保', '价格模式', '取价方式', '价格', '数量/权重', '备注','委托金额', '币种', 'BookCode'])
    order['市场'] = pd.Series(hold.index.map(lambda x: x[-2:])).replace({'SZ':1, 'SH':0})
    order['合约代码'] = pd.Series(hold.index.map(lambda x: x[:-3]))
    order['价格模式'] = 'ANY'
    order['数量/权重'] = hold.values
    order['委托方向'] = np.sign(order['数量/权重']).replace({1:'B', -1:'S'})
    order['数量/权重'] = order['数量/权重'].abs()
    order['价格'] = 0.0
    order['委托金额'] = 0.0
    order['币种'] = '00'
    order.to_excel('d:\\daily_report\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()), index=False)
holding = g6.iloc[-2:].dropna(axis=1, how='all').T


x1 = pd.DataFrame(g7).iloc[-1]
x2 = x1.pct_change()
x2 = x2.shift(-1)
x3 = pd.concat([x2.to_frame('strategy'), flow.index('s_dq_pctchange')], axis=1)
x3 = x3.loc['20201101':]
x4 = x3.resample('M').apply(lambda x: (x +1).cumprod().iloc[-1] -1)
x4 = x3.iloc[:, :-1].resample('M').apply(lambda x: (x +1).cumprod().iloc[-1] -1)
x4 = x3.iloc[:-1].resample('M').apply(lambda x: (x +1).cumprod().iloc[-1] -1)
