# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 13:52:16 2022

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
resid = -1 * barra.RESIDUAL_VOLATILITY()
resid.index.name = 'TRADE_DT'
returns = barra.stock('s_dq_pctchange')
momentum = -1 * returns.rolling(42, min_periods=30).mean().shift(3).stats.neutral(neu_axis=1, me=me).resid
indexs = barra.index('s_dq_pctchange')['000905.SH']

ic500 = flow.index_member('000905.SH', False)
if300 = flow.index_member('399300.SZ', False)

revenue = {'TOT_OPER_REV_TTM':finance.TOT_OPER_REV_TTM(), 'OPER_REV_TTM':finance.OPER_REV_TTM()}
profit = {'TOT_PROFIT_TTM':finance.TOT_PROFIT_TTM(), 'OPER_PROFIT_TTM': finance.OPER_PROFIT_TTM(), 'EBIT':finance.EBIT(), 'NET_PROFIT_TTM':finance.NET_PROFIT_TTM(), 'PAR_COMP_NET_INC_TTM':finance.PAR_COMP_NET_INC_TTM()}
growth = {'OPER_REV_GROWTH_RATIO': finance.OPER_REV_GROWTH_RATIO(), 'OPER_PROFIT_GROWTH_RATIO': finance.OPER_PROFIT_GROWTH_RATIO(), 'TOT_ASSET_GROWTH_RATIO':finance.TOT_ASSET_GROWTH_RATIO(), 'OPER_CASH_GROWTH_RATIO':finance.OPER_CASH_GROWTH_RATIO()}
equity = {'ROA_TTM':finance.ROA_TTM(), 'ROE_TTM':finance.ROE_TTM()}
cash = {'NET_OPER_CASH_TTM': finance.NET_OPER_CASH_TTM(), 'IM_NET_CASH_FLOWS_OPER_ACT': finance.IM_NET_CASH_FLOWS_OPER_ACT()}
assets = {'TOT_ASSETS':finance.TOT_ASSETS(), 'NET_ASSETS':finance.NET_ASSETS()}


revenue_values_500 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(ic500)[ic500.notnull()] for i,j in revenue.items()}, axis=1).stack().mean(axis=1).unstack() 
revenue_effect_500 = revenue_values_500.build.group().build.portfolio(returns).analysis.effective().shift()
revenue_effect_500 = revenue_effect_500.rolling(42).mean() /  revenue_effect_500.rolling(42).std()
revenue_effect_500 = revenue_effect_500[revenue_effect_500 > 0]

profit_values_500 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(ic500)[ic500.notnull()] for i,j in profit.items()}, axis=1).stack().mean(axis=1).unstack() 
profit_effect_500 = profit_values_500.build.group().build.portfolio(returns).analysis.effective().shift()
profit_effect_500 = profit_effect_500.rolling(42).mean() / profit_effect_500.rolling(42).std()
profit_effect_500 = profit_effect_500[profit_effect_500 > 0]

growth_values_500 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(ic500)[ic500.notnull()] for i,j in growth.items()}, axis=1).stack().mean(axis=1).unstack() 
growth_effect_500 = growth_values_500.build.group().build.portfolio(returns).analysis.effective().shift()
growth_effect_500 = growth_effect_500.rolling(42).mean() / growth_effect_500.rolling(42).std()
growth_effect_500 = growth_effect_500[growth_effect_500 > 0]

equity_values_500 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(ic500)[ic500.notnull()] for i,j in equity.items()}, axis=1).stack().mean(axis=1).unstack() 
equity_effect_500 = equity_values_500.build.group().build.portfolio(returns).analysis.effective().shift()
equity_effect_500 = equity_effect_500.rolling(42).mean() / equity_effect_500.rolling(42).std()
equity_effect_500 = equity_effect_500[equity_effect_500 > 0]

cash_values_500 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(ic500)[ic500.notnull()] for i,j in cash.items()}, axis=1).stack().mean(axis=1).unstack() 
cash_effect_500 = cash_values_500.build.group().build.portfolio(returns).analysis.effective().shift()
cash_effect_500 = cash_effect_500.rolling(42).mean() / cash_effect_500.rolling(42).std()
cash_effect_500 = cash_effect_500[cash_effect_500 > 0]

assets_values_500 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(ic500)[ic500.notnull()] for i,j in assets.items()}, axis=1).stack().mean(axis=1).unstack() 
assets_effect_500 = assets_values_500.build.group().build.portfolio(returns).analysis.effective().shift()
assets_effect_500 = assets_effect_500.rolling(42).mean() / assets_effect_500.rolling(42).std()
assets_effect_500 = assets_effect_500[assets_effect_500 > 0]

mom_500 = momentum.reindex_like(ic500)[ic500.notnull()]
mom_effect_500 = mom_500.build.group().build.portfolio(returns).analysis.effective().shift()
mom_effect_500 = mom_effect_500.rolling(42).mean() / mom_effect_500.rolling(42).std()
mom_effect_500 = mom_effect_500[mom_effect_500 > 0]

resid_500 = resid.reindex_like(ic500)[ic500.notnull()]
resid_effect_500 = resid_500.build.group().build.portfolio(returns).analysis.effective().shift()
resid_effect_500 = resid_effect_500.rolling(42).mean() / resid_effect_500.rolling(42).std()
resid_effect_500 = resid_effect_500[resid_effect_500 > 0]


rank_500 = pd.concat({'revenue':revenue_values_500.mul(revenue_effect_500, axis=0), 
                'profit':profit_values_500.mul(profit_effect_500, axis=0), 
                'growth':growth_values_500.mul(growth_effect_500, axis=0), 
                'equity':equity_values_500.mul(equity_effect_500, axis=0),
                'cash':cash_values_500.mul(cash_effect_500, axis=0), 
                'assets': assets_values_500.mul(assets_effect_500, axis=0), 
                'mom':mom_500.stats.standard(axis=1).mul(mom_effect_500, axis=0), 
                'resid':resid_500.stats.standard(axis=1).mul(resid_effect_500, axis=0)}, axis=1).stack().sum(axis=1, min_count = 1).unstack()
group_500 = rank_500.build.cut(75, 125, pct=False).astype(float).replace(0, np.nan).dropna(how='all', axis=1).reindex(returns.index)
#chain_500 = pd._DataFrame(group_500).shift()['2017-01-01':].chain()
effect_500 = rank_500.build.group().build.portfolio(returns, weight=ic500).analysis.effective().shift()




revenue_values_300 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(if300)[if300.notnull()] for i,j in revenue.items()}, axis=1).stack().mean(axis=1).unstack() 
revenue_effect_300 = revenue_values_300.build.group().build.portfolio(returns).analysis.effective().shift()
revenue_effect_300 = revenue_effect_300.rolling(42).mean() /  revenue_effect_300.rolling(42).std()
revenue_effect_300 = revenue_effect_300[revenue_effect_300 > 0]

profit_values_300 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(if300)[if300.notnull()] for i,j in profit.items()}, axis=1).stack().mean(axis=1).unstack() 
profit_effect_300 = profit_values_300.build.group().build.portfolio(returns).analysis.effective().shift()
profit_effect_300 = profit_effect_300.rolling(42).mean() / profit_effect_300.rolling(42).std()
profit_effect_300 = profit_effect_300[profit_effect_300 > 0]

growth_values_300 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(if300)[if300.notnull()] for i,j in growth.items()}, axis=1).stack().mean(axis=1).unstack() 
growth_effect_300 = growth_values_300.build.group().build.portfolio(returns).analysis.effective().shift()
growth_effect_300 = growth_effect_300.rolling(42).mean() / growth_effect_300.rolling(42).std()
growth_effect_300 = growth_effect_300[growth_effect_300 > 0]

equity_values_300 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(if300)[if300.notnull()] for i,j in equity.items()}, axis=1).stack().mean(axis=1).unstack() 
equity_effect_300 = equity_values_300.build.group().build.portfolio(returns).analysis.effective().shift()
equity_effect_300 = equity_effect_300.rolling(42).mean() / equity_effect_300.rolling(42).std()
equity_effect_300 = equity_effect_300[equity_effect_300 > 0]

cash_values_300 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(if300)[if300.notnull()] for i,j in cash.items()}, axis=1).stack().mean(axis=1).unstack() 
cash_effect_300 = cash_values_300.build.group().build.portfolio(returns).analysis.effective().shift()
cash_effect_300 = cash_effect_300.rolling(42).mean() / cash_effect_300.rolling(42).std()
cash_effect_300 = cash_effect_300[cash_effect_300 > 0]

assets_values_300 = pd.concat({i:j.values.rank(axis=1, pct=True).reindex_like(if300)[if300.notnull()] for i,j in assets.items()}, axis=1).stack().mean(axis=1).unstack() 
assets_effect_300 = assets_values_300.build.group().build.portfolio(returns).analysis.effective().shift()
assets_effect_300 = assets_effect_300.rolling(42).mean() / assets_effect_300.rolling(42).std()
assets_effect_300 = assets_effect_300[assets_effect_300 > 0]

mom_300 = momentum.reindex_like(if300)[if300.notnull()]
mom_effect_300 = mom_300.build.group().build.portfolio(returns).analysis.effective().shift()
mom_effect_300 = mom_effect_300.rolling(42).mean() / mom_effect_300.rolling(42).std()
mom_effect_300 = mom_effect_300[mom_effect_300 > 0]

resid_300 = resid.reindex_like(if300)[if300.notnull()]
resid_effect_300 = resid_300.build.group().build.portfolio(returns).analysis.effective().shift()
resid_effect_300 = resid_effect_300.rolling(42).mean() / resid_effect_300.rolling(42).std()
resid_effect_300 = resid_effect_300[resid_effect_300 > 0]


rank_300 = pd.concat({'revenue':revenue_values_300.mul(revenue_effect_300, axis=0),
                'profit':profit_values_300.mul(profit_effect_300, axis=0), 
                'growth':growth_values_300.mul(growth_effect_300, axis=0), 
                'equity':equity_values_300.mul(equity_effect_300, axis=0),
                'cash':cash_values_300.mul(cash_effect_300, axis=0), 
                'assets': assets_values_300.mul(assets_effect_300, axis=0), 
                'mom': mom_300.stats.standard(axis=1).mul(mom_effect_300, axis=0), 
                'resid': resid_300.stats.standard(axis=1).mul(resid_effect_300, axis=0)}, axis=1).stack().sum(axis=1, min_count=1).dropna().unstack()
group_300 = if300[rank_300.build.cut(20, 70, pct=False).dropna(how='all', axis=1).reindex(returns.index)].dropna(how='all', axis=1)
#chain_300 = pd._DataFrame(group_300).shift()['2017-01-01':].chain()
effect_300 = rank_300.build.group().build.portfolio(returns, weight=if300).analysis.effective().shift()


revenue_values_3000 = pd.concat({i:j.values.rank(axis=1, pct=True) for i,j in revenue.items()}, axis=1).stack().mean(axis=1).unstack() 
revenue_effect_3000 = revenue_values_3000.build.group().build.portfolio(returns).analysis.effective().shift()
revenue_effect_3000 = revenue_effect_3000.rolling(42).mean() /  revenue_effect_3000.rolling(42).std()
revenue_effect_3000 = revenue_effect_3000[revenue_effect_3000 > 0]

profit_values_3000 = pd.concat({i:j.values.rank(axis=1, pct=True) for i,j in profit.items()}, axis=1).stack().mean(axis=1).unstack() 
profit_effect_3000 = profit_values_3000.build.group().build.portfolio(returns).analysis.effective().shift()
profit_effect_3000 = profit_effect_3000.rolling(42).mean() / profit_effect_3000.rolling(42).std()
profit_effect_3000 = profit_effect_3000[profit_effect_3000 > 0]

growth_values_3000 = pd.concat({i:j.values.rank(axis=1, pct=True) for i,j in growth.items()}, axis=1).stack().mean(axis=1).unstack() 
growth_effect_3000 = growth_values_3000.build.group().build.portfolio(returns).analysis.effective().shift()
growth_effect_3000 = growth_effect_3000.rolling(42).mean() / growth_effect_3000.rolling(42).std()
growth_effect_3000 = growth_effect_3000[growth_effect_3000 > 0]

equity_values_3000 = pd.concat({i:j.values.rank(axis=1, pct=True) for i,j in equity.items()}, axis=1).stack().mean(axis=1).unstack() 
equity_effect_3000 = equity_values_3000.build.group().build.portfolio(returns).analysis.effective().shift()
equity_effect_3000 = equity_effect_3000.rolling(42).mean() / equity_effect_3000.rolling(42).std()
equity_effect_3000 = equity_effect_3000[equity_effect_3000 > 0]

cash_values_3000 = pd.concat({i:j.values.rank(axis=1, pct=True) for i,j in cash.items()}, axis=1).stack().mean(axis=1).unstack() 
cash_effect_3000 = cash_values_3000.build.group().build.portfolio(returns).analysis.effective().shift()
cash_effect_3000 = cash_effect_3000.rolling(42).mean() / cash_effect_3000.rolling(42).std()
cash_effect_3000 = cash_effect_3000[cash_effect_3000 > 0]

assets_values_3000 = pd.concat({i:j.values.rank(axis=1, pct=True) for i,j in assets.items()}, axis=1).stack().mean(axis=1).unstack() 
assets_effect_3000 = assets_values_3000.build.group().build.portfolio(returns).analysis.effective().shift()
assets_effect_3000 = assets_effect_3000.rolling(42).mean() / assets_effect_3000.rolling(42).std()
assets_effect_3000 = assets_effect_3000[assets_effect_3000 > 0]

mom_3000 = momentum
mom_effect_3000 = mom_3000.build.group().build.portfolio(returns).analysis.effective().shift()
mom_effect_3000 = mom_effect_3000.rolling(42).mean() / mom_effect_3000.rolling(42).std()
mom_effect_3000 = mom_effect_3000[mom_effect_3000 > 0]

resid_3000 = resid
resid_effect_3000 = resid_3000.build.group().build.portfolio(returns).analysis.effective().shift()
resid_effect_3000 = resid_effect_3000.rolling(42).mean() / resid_effect_3000.rolling(42).std()
resid_effect_3000 = resid_effect_3000[resid_effect_3000 > 0]


rank_3000 = pd.concat({'revenue':revenue_values_3000.rank(axis=1, pct=True).mul(revenue_effect_3000, axis=0), 
                'profit':profit_values_3000.rank(axis=1, pct=True).mul(profit_effect_3000, axis=0), 
                'growth':growth_values_3000.rank(axis=1, pct=True).mul(growth_effect_3000, axis=0), 
                'equity':equity_values_3000.rank(axis=1, pct=True).mul(equity_effect_3000, axis=0),
                'cash':cash_values_3000.rank(axis=1, pct=True).mul(cash_effect_3000, axis=0), 
                'assets': assets_values_3000.rank(axis=1, pct=True).mul(assets_effect_3000, axis=0), 
                'mom':mom_3000.rank(axis=1, pct=True).mul(mom_effect_3000, axis=0), 
                'resid':resid_3000.rank(axis=1, pct=True).mul(resid_effect_3000, axis=0)}, axis=1).stack().sum(axis=1, min_count = 1).unstack()
group_3000 = rank_3000.build.cut(50, 100, pct=False).dropna(how='all', axis=1).reindex(returns.index)
#chain_3000 = pd._DataFrame(group_3000).shift()['2016-09-30':].chain()
effect_3000 = rank_3000.build.group().build.portfolio(returns).analysis.effective().shift()





weight = [effect_300, effect_500, effect_3000]
weight = pd.concat(weight, axis=1).reindex(returns.index)
weight = weight.rolling(63).mean() / weight.rolling(63).std()
weight.columns = ['group_300', 'group_500', 'group_3000']
weight = weight.sub(weight.min(axis=1), axis=0).div(weight.max(axis=1) - weight.min(axis=1), axis=0)
weight = weight.div(weight.sum(axis=1), axis=0)
weight = weight * 0.85 + 0.05
weight = weight.rolling(3).mean()
weight['group_300'] = weight['group_300'] * 2

factors = pd.concat({'group_300':group_300, 'group_500':group_500, 'group_3000':group_3000}, axis=1).astype(float).replace(0, np.nan).stack()
factors = (factors * weight).sum(axis=1, min_count=1).unstack().dropna(how='all', axis=1)

factor_chain = pd._DataFrame(factors).shift()['2017-01-01':].chain()






