# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 15:19:04 2021

@author: Porco Rosso
"""

'''
import pandas as pd
import __pandas
import numpy as np
import flow
returns = flow.stock('s_dq_pctchange')
mv = flow.stock('s_val_mv')
ind = flow.stock('s_swl1_code')
factor = flow.stock('OPER_PROFIT_TTM')
factor_diff = factor.diff().replace(0, np.nan).fillna(method='ffill', limit=100)
factor.columns = pd.MultiIndex.from_product([['factor'], factor.columns])
factor_diff.columns = pd.MultiIndex.from_product([['factor_diff'], factor_diff.columns])
ind.columns = pd.MultiIndex.from_product([['indust'], ind.columns])
mv.columns = pd.MultiIndex.from_product([['mv'], mv.columns])
obj = pd.concat([factor, factor_diff, ind, mv], axis=1)
obj = obj.stack('S_INFO_WINDCODE')
obj = obj.reset_index()
obj['ind_mv_group'] = obj['factor'] / obj['mv']
obj['ind_mv_group'][(obj['factor_diff'] < 0) | (obj['ind_mv_group'] < 0)] = np.nan

obj['ind_mv_group'] =  obj.groupby(['TRADE_DT', 'indust'])['ind_mv_group'].rank(pct=True)
obj = obj.set_index(['TRADE_DT', 'S_INFO_WINDCODE'])

------------------------------------------------------------------------------

001 NET_OPER_CAP
    
    building:
        factor = NET_OPER_CAP.diff()
    periods:
        2014 - 2021
    effective:
        black
    describe:
        净运营资本：	流动资产 - 流动负债
    
            fator |      < 0      |    >=0
            ----------------------------------
        t    0      -0.001411       0.00067506
             1      -0.000532  
             2       0.000133
             3       0.000372
             4       0.000984
        
------------------------------------------------------------------------------







003 OPER_PROFIT_TTM

    building:
        factor = OPER_PROFIT_TTM.diff()
    periods:
        2014 - 2021
    effective:
        white
        black
    describe:
        营业利润TTM: 计算过去12个月 营业利润 之和
        
            factor |     < 0     |     = 0     |     > 0    
            -------------------------------------------------
        t   -4       0.001543                     0.0027
            -3       0.002804                     0.003463
            -2       0.002631                     0.004577
            -1       0.002379                     0.004221
             0      -0.005057      0.000683       0.003402
             1      -0.001028                     0.002131
             2      -8.9e-05                      0.002793
             3      -2.1e-05                      0.001354
             4       0.00084                      0.00169 

------------------------------------------------------------------------------

004 NET_OPER_CASH_TTM

    building:
        factor = NET_OPER_CASH_TTM.diff()
    periods:
        2014 - 2021
    effective:
        black
    describe:
        经营活动现金流量净额TTM: 计算过去12个月 经营活动产生的现金流量净值 之和

            fator |      < 0      |    >=0
            ----------------------------------
        t    0      -0.001062       0.00068
             1       7e-05  

------------------------------------------------------------------------------

005 OPER_REV_TTM



















'''
