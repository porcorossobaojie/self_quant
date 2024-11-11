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
from __factors__.equity import main as equity

import __data__
import __trade__
import flow

if __name__ == '__main__':
    count = 30
    path = 'd:\\strategys_data\\volitility\\strategy_002'
    __data__.joinquant.daily()
    
    equity_obj = equity.main()
    equity_obj.data_init()
    fin_001 = equity_obj.fac_001()
    fin_002 = equity_obj.fac_002()
    
    tech_obj = trading_v001.main()
    tech_obj.data_init()
    tech_001 = equity_obj.__filter__(tech_obj.fac_001())
    tech_002 = equity_obj.__filter__(tech_obj.abnormal1())
    
    
    fac_obj = tech_001 + 0.1 *(tech_002 + fin_001 - fin_002)
    fac = fac_obj.copy()
    fac = fac.loc[:, [i[:3] not in ['002', '300', '688', '301'] for i in fac.columns]]
    #fac = fac.fillna(tech_001)
    fac = fac.rollings(21).min(3).mean()

    try:
        file_list = os.listdir(path)
        if len(file_list):
            pd._Series.data_source.internal_data
            hold_list = sorted([i for i in file_list if 'hold' in i])
            order_list = sorted([i for i in file_list if 'order' in i])
            hold_list = [pd.read_excel(path + '\\' + i, usecols=[1,4], dtype={0:str, 1:float}).rename({'代码':'S_INFO_WINDCODE', '持仓数量': pd.to_datetime(i.split('_')[-1][:-5] + ' 15:00:00')}, axis=1) for i in hold_list]
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
        order.to_excel(path + '\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        total_order =  pd._Series(fac.iloc[-1].nlargest(count).notnull(), is_adj=False).settle.assets(hold_list[1].settle.tot_assets()).settle.share().round(-2)
        total_order = total_order.sub(hold_list[1]).dropna()
        fac_rank = fac.iloc[-1].rank(ascending=False)
        total_order = pd.concat([total_order, fac_rank.nsmallest(count).rename('fac_value')], axis=1)
        total_order.iloc[:, -1] =  total_order.iloc[:, -1].fillna(fac_rank)
        total_order = total_order.sort_values('fac_value')
        total_order.to_excel(path + '\\total_order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        from __trade__.main.main import link as link
        returns = link(order=hold_list[1].day_shift(-1), hold=hold_list[0])
        print(returns.returns, round(returns.done.settle.tot_assets() - returns.hold.settle.tot_assets(), 2))
        print(1)
        
    except:
        portfolio = fac.build.cut(count, 250, pct=False)
        test_obj = pd._DataFrame(portfolio).loc['2017':].chain()
        hold = portfolio.iloc[-2:].astype(float).replace(0, np.nan).dropna(how='all', axis=1).T
        order = pd._Series(hold.iloc[:, -1].dropna()).settle.assets(970000).settle.share().recover().round(-2)
        order.to_excel(path + '\\order_%s.xlsx' %(pd.Timestamp.now().date().__str__()))
        print(2)

