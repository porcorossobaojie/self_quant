# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:19:33 2023

@author: Porco Rosso
"""

import __pandas
import pandas as pd
import numpy as np
import os
from __factors__.market import trading_v001
from __factors__.finance import indust_index

import __data__
import __trade__
import flow

if __name__ == '__main__':
    count = 30
    path = 'd:\\strategys_data\\multi_factors_voli_mean\\'
    __data__.joinquant.daily()
    
    vol_obj = trading_v001.main()
    vol_obj.data_init()
    vol_fac001 = vol_obj.fac_001()
    
    ind_obj = indust_index.main()
    ind_obj.data_init()
    ind_fac001 = ind_obj.fac_001()
    
    fac_obj = (vol_fac001.rank(pct=True, axis=1) ** 2 * 2 + ind_fac001.rank(pct=True, axis=1) ** 2)
    fac_obj = (vol_fac001.rolling(512, min_periods=252).rank(pct=True) ** 2 * 2 + ind_fac001.rolling(512, min_periods=252).rank(pct=True) ** 2)
    fac_obj = fac_obj.dropna(axis=1, how='all')
    fac = fac_obj.copy()
    fac = vol_obj.__filter__(fac)
    fac = fac.loc[:, [i[:3] not in ['002', '300', '688'] for i in fac.columns]]
    fac = fac.rollings(21).min(3).mean()

    try:
        file_list = os.listdir(path)
        if len(file_list):
            pd._Series.data_source.internal_data
            hold_list = sorted([i for i in file_list if 'hold' in i])
            order_list = sorted([i for i in file_list if 'order' in i])
            hold_list = [pd.read_excel(path + i, usecols=[1,4], dtype={0:str, 1:float}).rename({'代码':'S_INFO_WINDCODE', '持仓数量': pd.to_datetime(i.split('_')[-1][:-5] + ' 15:00:00')}, axis=1) for i in hold_list]
            for i in hold_list:
                i.iloc[:, 0] = __data__.joinquant.joinquant.normalize_code(i.iloc[:, 0].to_list())
                i.iloc[:, 0] = i.iloc[:, 0].str.replace('XSHG', 'SH')
                i.iloc[:, 0] = i.iloc[:, 0].str.replace('XSHE', 'SZ')
            hold_list = [pd._Series(i.set_index('S_INFO_WINDCODE').T.iloc[0], state='settle', unit='share', is_adj=False) for i in hold_list]
        portfolio = fac.iloc[-2:].copy()
        portfolio.iloc[0][hold_list[1].reindex_like(portfolio.iloc[0]).isnull()] = np.nan
        portfolio = portfolio.build.cut(count, 250, pct=False)
        order = pd._Series(portfolio.iloc[-1][portfolio.iloc[-1]], is_adj=False).settle.assets(hold_list[1].settle.tot_assets()).settle.share().round(-2)
        order = order.sub(hold_list[1]).replace(0, np.nan).dropna()
        order = order.to_frame()
        order['position'] = np.where(order.iloc[:, -1] > 0, 'b', 's')
        order.to_excel(path + 'order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        total_order =  pd._Series(fac.iloc[-1].nlargest(count).notnull(), is_adj=False).settle.assets(hold_list[1].settle.tot_assets()).settle.share().round(-2)
        total_order = total_order.sub(hold_list[1]).dropna()
        fac_rank = fac.iloc[-1].rank(ascending=False)
        total_order = pd.concat([total_order, fac_rank.nsmallest(count).rename('fac_value')], axis=1)
        total_order.iloc[:, -1] =  total_order.iloc[:, -1].fillna(fac_rank)
        total_order = total_order.sort_values('fac_value')
        total_order.to_excel(path + 'total_order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        from __trade__.main.main import link as link
        returns = link(order=hold_list[1], hold=hold_list[0])
        print(returns.returns, round(returns.done.settle.tot_assets() - returns.hold.settle.tot_assets(), 2))
        print(1)
        
    except:
        print(2)
        portfolio = fac.build.cut(count, 250, pct=False)
        test_obj = pd._DataFrame(portfolio).loc['2017':].chain()


