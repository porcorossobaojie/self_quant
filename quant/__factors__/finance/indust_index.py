# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 09:38:14 2023

@author: Porco Rosso
"""

import flow
from __factors__ import barra

from __factors__.base.main import main as meta
from __factors__.finance.config import main as config
from __pandas.__stats.__obj import __neutral as neutral
import pandas as pd
import numpy as np

class main(meta):
    group = 'S_JQL2_CODE'

    def data_init(self):
        self.initialize(**config.params)
        
    def _group_func(self, df, weight=None, group=None, how='sum', col='S_INFO_WINDCODE'):
        col = col.upper()
        group = self.group if group is None else group
        group_obj = {0: df, 1:(self.stock(group) if isinstance(group, str) else group)}
        if weight is not None:
            weight_df = self.stock(weight) if isinstance(weight, str) else weight.copy()
            group_obj[2] = weight_df    
            group_obj = pd.concat(group_obj, axis=1).stack()
        else:
            group_obj = pd.concat(group_obj, axis=1).stack()
            group_obj[2] = 1    
        group_obj = group_obj[group_obj[1].notnull()]
        group_obj[0] = group_obj[0] * group_obj[2]
        group_obj[2] = group_obj[2][group_obj[0].notnull()]
        if col == 'S_INFO_WINDCODE':
            out_obj = group_obj.groupby(['TRADE_DT', 1])[0, 2].transform('sum', min_count=1)
        else:
            out_obj =  group_obj.groupby(['TRADE_DT', 1])[0, 2].sum(min_count=1)
        if how == 'mean':
            out_obj = (out_obj[0] / out_obj[2]).unstack()
        elif how == 'sum':
            out_obj = out_obj[0].unstack()
        out_obj.columns.name = col
        return out_obj
    
    def _expose(self, df, group=None):
        group = self.group if group is None else group
        group = self.stock(group) if isinstance(group, str) else group
        group = group.stack().to_frame('S_INFO_INDCODE')
        df = df.stack()
        df = df.to_frame('value') if isinstance(df, pd.Series) else df
        df = pd.merge(group, df, left_on=['TRADE_DT', 'S_INFO_INDCODE'], right_index=True, how='left')
        df = df.iloc[:, 1:]
        df = df if len(df.columns) > 1 else df.iloc[:, 0]
        df = df.unstack().sort_index(axis=1)
        return df
            
    def returns(self, col='S_INFO_INDCODE'):
        returns = self.__filter__(self.stock('s_dq_pctchange'))
        weight = np.log(self.stock('s_val_mv').shift())
        df = self._group_func(returns, weight, self.group, how='mean', col=col)
        return df
    
    def _prem(self, target_df, group=None, periods=126, how='multi',  **key_prems):
        group = self.group if group is None else group
        group_obj = {0: target_df, 1:(self.stock(group).fillna(method='bfill', limit=252) if isinstance(group, str) else group)}
        if len(key_prems):
            group_obj.update(key_prems)
            group_obj = pd.concat(group_obj, axis=1)
            group_obj = group_obj.stack()
            def func(df, period):
                df[1] = 1
                x = df.unstack()
                values = np.array([x.iloc[i: i+period].values for i in range(x.shape[0] - period)])
                values = values.transpose(0, 2, 1).reshape(values.shape[0], df.shape[1], -1).transpose(0,2,1)
                values = values - np.nanmean(values, axis=1).reshape(values.shape[0], 1, values.shape[-1])
                values[:, :, 1] = 1
                if how == 'simple':
                    params = {j: neutral(values[:, :, [0, 1, i]])[:, 1] for i,j in enumerate(df.columns[2:], 2)}
                    params = pd.DataFrame(params, index=x.index[period:])
                elif how == 'multi':
                    params = neutral(values)[:, 1:]
                    params = pd.DataFrame(params, index=x.index[period:], columns=df.columns[2:])
                return params
            dic = {}
            for i,j in group_obj.groupby(1):
                dic[i] = func(j, periods)
            dic = pd.concat(dic)
            dic.index.names = ['S_INFO_INDCODE', 'TRADE_DT']
            dic = dic.swaplevel('TRADE_DT', 'S_INFO_INDCODE')
            return dic
        else:
            return pd.DataFrame()
    
    def _log(self, df, abs=True, add=1):
        df = (np.sign(df) if abs else 1) * np.log((df.abs() if abs else df) + add)
        return df
        
    
    def finance_factors(self, log=True):
        dic = {}
        dic['oper'] = flow.stock('tot_oper_rev_ttm')
        dic['profit'] = flow.stock('TOT_PROFIT_TTM')
        dic['asset'] = flow.stock_finance('TOT_ASSETS', shift=6)
        dic['cash'] = flow.stock('NET_OPER_CASH_TTM')
        dic['oper_gth'] = flow.stock('OPER_REV_GROWTH_RATIO')        
        dic['profit_gth'] = flow.stock('OPER_REV_GROWTH_RATIO')
        dic['asset_gth'] = flow.stock('TOT_ASSET_GROWTH_RATIO')
        dic['cash_gth'] = flow.stock('OPER_CASH_GROWTH_RATIO').fillna(method='ffill', limit=126)
        if log:
            dic = {'log_' + i : self._log(j) for i,j in dic.items()}
        return dic
    
    def mv(self, log=True):
        df = self.stock('S_VAL_MV')
        if log:
            df = self._log(df)
        return df
    
    def index_prem(self, target_df=None, factors=None, log=True, periods=126):
        if target_df is None:
            target_df = self.mv(log)
        else:
            target_df = self._log(target_df) if log else target_df
        if factors is None:
            factors = self.finance_factors(log)
        else:
            factors = self._log(factors) if log else factors
            
        df = self._prem(target_df, periods=periods, how='multi', **factors)
        df = self._expose(df.unstack())
        facs = pd.concat(factors, axis=1)
        df = (df * facs).stack().sum(axis=1, min_count=len(factors)).unstack().sort_index(axis=1)
        return df
    
    def fac_001(self, group='S_JQL1_CODE'):
        mv = self.mv()
        dic = self.finance_factors()
        prem = self.index_prem()
        mv_mean = self._group_func(self._log(mv), how='mean')
        prems = prem + mv_mean
        prems_momentum = prems
        dic['ind_index'] = prem
        df = mv.stats.neutral(neu_axis=1,  **dic)
        df = (mv - df.resid) / mv
        df = barra.barra_neutral(df)
        ind_rank = pd.concat({'ind':flow.stock(group), 'fac':df}, axis=1)
        ind_rank = ind_rank.stack().groupby(['TRADE_DT', 'ind']).rank(pct=True).iloc[:, 0].unstack()
        df = df.rank(axis=1,pct=True) + ind_rank
        return df
'''        
        
if __name__ == '__main__':
    self = main()
    self.data_init()
    log_mv = flow.stock('s_val_mv')
    log_mv = self._log(flow.stock('s_val_mv'))
    log_oper = self._log(flow.stock('tot_oper_rev_ttm'))
    log_profit = self._log(flow.stock('TOT_PROFIT_TTM'))
    log_asset = self._log(flow.stock_finance('tot_assets', shift=4))
    log_cash = self._log(flow.stock('NET_OPER_CASH_TTM'))
    oper_grow = self._log(flow.stock('OPER_REV_GROWTH_RATIO'))
    profit_grow = self._log(flow.stock('OPER_PROFIT_GROWTH_RATIO'))
    asset_grow = self._log(flow.stock('TOT_ASSET_GROWTH_RATIO'))
    cash_grow = self._log(flow.stock('OPER_CASH_GROWTH_RATIO'))    
    dic = {'log_oper':log_oper, 'log_profit': log_profit, 'log_asset':log_asset, 'log_cash':log_cash, 'oper_grow':oper_grow, 'profit_grow':profit_grow, 'asset_grow':asset_grow, 'cash_grow':cash_grow}
    prem = self._prem(log_mv, periods=126, how='multi', **dic)
    g1 = self._expose(prem.unstack())
    g2 = pd.concat(dic, axis=1)
    g3 = g1 * g2
    g3 = g3.stack()
    g3 = g3.sum(axis=1, min_count=8)
    g3  =g3.unstack()
    g3 = g3.sort_index(axis=1)
    dic['indust'] = g3
    x1 = log_mv.stats.neutral(neu_axis=1,  **dic)
    x2 = log_mv - x1.resid   
    x3 = x2 / log_mv
    ind = flow.stock('s_jql1_code')
    f2 = pd.concat({'ind':ind, 'x3':trading_v001.barra.barra_neutral(x3)}, axis=1)
    f2 = f2.stack()    
    f2 = f2.groupby(['TRADE_DT', 'ind']).rank(pct=True)
    f2  = f2.iloc[:, 0].unstack()
    ff  = f2.rank(pct=True) ** 2 + fac001.rank(pct=True) ** 2  * 2
    ff1 = ff.rollings(21).min(3).mean()
    ff1 = ff1.reindex_like(returns)
    ff2 = ff1.build.cut(50, 250, pct=False)    
    ff3  = pd._DataFrame(ff2).loc['2018':].chain()
'''    
    
