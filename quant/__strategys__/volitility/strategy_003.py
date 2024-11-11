# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:41:06 2022

@author: Porco Rosso
"""

import __pandas
import pandas as pd
import numpy as np
from __factors__.market import trading_v001

import __data__
import __trade__
import flow

if __name__ == '__main__':
    __data__.joinquant.daily()
    fac_obj = trading_v001.main()
    fac_obj.data_init()
    fac001 = fac_obj.fac_001()
    fac002 = fac_obj.abnormal1()
    returns = flow.stock('s_dq_pctchange')
    fac001_stand = fac_obj.__filter__(fac001).stats.standard(axis=1)
    fac002_stand = fac_obj.__filter__(fac002).stats.standard(axis=1)
    params1 = returns.shift().stats.neutral(neu_axis=1, fac=fac001_stand).params.iloc[:, 1]
    params2 = returns.shift().stats.neutral(neu_axis=1, fac=fac002_stand).params.iloc[:, 1]
    params1 = (np.exp(params1) - 0.95) / (1 + np.exp(params1))
    params2 = (np.exp(params2) - 0.95) / (1 + np.exp(params2))
    fac = fac001_stand.mul(params1.rolling(5).mean(), axis=0) + fac002_stand.mul(params2.rolling(5).mean(), axis=0)
    fac = fac_obj.__filter__(fac)
    fac = fac.loc[:, [i[:3] not in ['002', '300', '688', '301'] for i in fac.columns]]
    fac = fac.rollings(10).min(2).mean()
    #fac = fac.rollings(10).min(2).mean()
    count = 24

    try:
        '''
        hold = pd.read_excel('d:\\oth_daily_report\\hold_%s.xlsx' %(pd.Timestamp.now().date().__str__()), usecols=[1,4], dtype={0:str, 1:float}, thousands=',')
        hold.columns = ['S_INFO_WINDCODE', flow.trade_days()[-2]]
        hold.iloc[:, 0] = __data__.joinquant.joinquant.normalize_code(hold.iloc[:, 0].to_list())
        hold.iloc[:, 0] = hold.iloc[:, 0].str.replace('XSHG', 'SH')
        hold.iloc[:, 0] = hold.iloc[:, 0].str.replace('XSHE', 'SZ')
        hold = hold.set_index('S_INFO_WINDCODE').T

        
        pd._Series.data_source.internal_data
        portfolio = fac.iloc[-2:]
        portfolio.iloc[[0]] = portfolio.iloc[[0]][hold.reindex_like(portfolio.iloc[[0]]).notnull()]
        portfolio = portfolio.build.cut(27, 250, pct=False)
        portfolio = portfolio[portfolio].dropna(how='all', axis=1).astype(float)
        hold = pd._Series(hold.iloc[0], unit='share', is_adj=False).day_shift()
        order = pd._Series(portfolio.iloc[-1].dropna(), is_adj=False).settle.assets(hold.settle.tot_assets()).settle.share().round(-2)
        order = order.sub(hold).replace(0, np.nan).dropna()
        order = order.to_frame()
        order['position'] = np.where(order.iloc[:, -1] > 0, 'b', 's')
        order.to_excel('d:\\oth_daily_report\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        print(hold.settle.tot_assets() / hold.day_shift(-1).settle.tot_assets() - 1)
        print(1)
        '''
        
        lst = []
        for i in [-2, -1]:
            df = pd.read_excel('d:\\oth_daily_report\\hold_%s.xlsx' %(flow.trade_days()[i].date().__str__()), usecols=[1,4], dtype={0:str, 1:float}, thousands=',')
            df.columns = ['S_INFO_WINDCODE', flow.trade_days()[-2]]
            df.iloc[:, 0] = __data__.joinquant.joinquant.normalize_code(df.iloc[:, 0].to_list())
            df.iloc[:, 0] = df.iloc[:, 0].str.replace('XSHG', 'SH')
            df.iloc[:, 0] = df.iloc[:, 0].str.replace('XSHE', 'SZ')
            df = pd._Series(df.set_index('S_INFO_WINDCODE').T.iloc[0], state='settle', unit='share', is_adj=False)
            lst.append(df)
        
        pd._Series.data_source.internal_data
        portfolio = fac.iloc[-2:]
        portfolio.iloc[0][lst[1].reindex_like(portfolio.iloc[0]).isnull()] = np.nan
        portfolio = portfolio.build.cut(count, 250, pct=False)
        order = pd._Series(portfolio.iloc[-1][portfolio.iloc[-1]], is_adj=False).settle.assets(lst[1].settle.tot_assets()).settle.share().round(-2)
        order = order.sub(lst[1]).replace(0, np.nan).dropna()
        order = order.to_frame()
        order['position'] = np.where(order.iloc[:, -1] > 0, 'b', 's')
        order.to_excel('d:\\oth_daily_report\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        total_order =  pd._Series(fac.iloc[-1].nlargest(count).notnull(), is_adj=False).settle.assets(lst[1].settle.tot_assets()).settle.share().round(-2)
        total_order = total_order.sub(lst[1]).dropna()
        fac_rank = fac.iloc[-1].rank(ascending=False)
        total_order = pd.concat([total_order, fac_rank.nsmallest(count).rename('fac_value')], axis=1)
        total_order.iloc[:, -1] =  total_order.iloc[:, -1].fillna(fac_rank)
        total_order = total_order.sort_values('fac_value')
        total_order.to_excel('d:\\oth_daily_report\\total_order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        
        from __trade__.main.main import link as link
        returns = link(order=lst[1], hold=lst[0])
        print(returns.returns, round(returns.done.settle.tot_assets() - returns.hold.settle.tot_assets(), 2))
        print(1)
        
        
    except:
        portfolio = fac.build.cut(count, 250, pct=False)
        test_obj = pd._DataFrame(portfolio).loc['2017':].chain()
        hold = portfolio.iloc[-2:].astype(float).replace(0, np.nan).dropna(how='all', axis=1).T
        order = pd._Series(fac.iloc[-1].dropna().sort_values(ascending=False).iloc[:count]).settle.assets(700000).settle.share().recover().round(-2)
        order.to_excel('d:\\oth_daily_report\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        #g1 = fac.iloc[-1].sort_values(ascending=False)
        #g1.iloc[:count].to_excel('d:\\oth_daily_report\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        print(2)








