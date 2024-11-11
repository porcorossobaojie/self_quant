# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 17:45:54 2022

@author: Porco Rosso
"""

import flow
from __factors__ import barra

from __factors__.base.main import main as meta
from __factors__.equity.config import main as config
from __pandas.__stats.__obj import __neutral as neutral
import pandas as pd
import numpy as np

class main(meta):
    group = 'S_JQL1_CODE'
        
    def data_init(self):
        self.initialize(**config.params)
        
    def _group_func(self, df, weight=None, group=None, how='sum', col='S_INFO_WINDCODE'):
        col = col.upper()
        group = self.group if group is None else group
        group_obj = {0: df, 1:(self.stock(group) if isinstance(group, str) else group)}
        if how == 'std':
            group_obj = pd.concat(group_obj, axis=1).stack()
            if col == 'S_INFO_WINDCODE':
                out_obj = group_obj.groupby(['TRADE_DT', 1])[0].transform('std').unstack()
            else:
                out_obj =  group_obj.groupby(['TRADE_DT', 1])[0].std().unstack()
            return out_obj
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
    
    def _prem(self, target_df, group=None, periods=21,  **key_prems):
        group = self.group if group is None else group
        group_obj = {0: target_df, 1:(self.stock(group).fillna(method='bfill', limit=252) if isinstance(group, str) else group)}
        if len(key_prems):
            group_obj.update(key_prems)
            group_obj = pd.concat(group_obj, axis=1)
            group_obj = group_obj.stack()
            def func(df, period):
                df[1] = 1
                x = df.unstack()
                values = x.astype('float32').values
                values = np.array([values[i: i+period, :] for i in range(values.shape[0] - period)])
                values = values.transpose(0, 2, 1).reshape(values.shape[0], df.shape[1], -1).transpose(0,2,1)
                values = values - np.nanmean(values, axis=1).reshape(values.shape[0], 1, values.shape[-1])
                values[:, :, 1] = 1
                params = neutral(values)
                params = pd.DataFrame(params, index=x.index[period:], columns=df.columns[1:])
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
    
    def _finance_standard(self, key, shift, fillna, log, **kwargs):
        df = flow.stock_finance(key, shift=shift, **kwargs)
        df = df.fillna(fillna)                
        if log:
            df = self._log(df)
        return df

    def _finance_gth(self, key, shift, fillna, log, periods, **kwargs):
        df = self._finance_standard(key, shift, np.nan, log, periods=periods, **kwargs)
        df = df.groupby(df.index.names[0]).fillna(method='ffill', limit=periods-2)
        if log:
            df = df.groupby(df.index.names[0]).diff()
        else:
            df = df.groupby(df.index.names[0]).pct_change(fill_method=None)
            df = df[df.abs() != np.inf]
        df = df[df.index.get_level_values(1) == periods]
        df.index = df.index.get_level_values(0)
        df = df.fillna(fillna)
        return df

    def Fac_inventories(self):
        shift = 4
        log = True
        periods = 4
        assets_key = 'TOT_ASSETS'
        assets = self._finance_standard(assets_key, shift, fillna=np.nan, log=log)
        mv = self._log(flow.stock('s_val_mv'))

        inventory_key = 'INVENTORIES'
        inventory = self._finance_standard(inventory_key, shift, fillna=0, log=log)
        inventory_gth = self._finance_gth(inventory_key, shift, fillna=0, log=log, periods=periods)
        inv_to_assets = inventory / assets
        
        dic =  {'inventory':inventory, 'inventory_gth':inventory_gth, 'inv_to_assets':inv_to_assets, 'level':inventory.rank(axis=1, pct=True) * inventory_gth.rank(axis=1, pct=True)}
        params = self._prem(mv, **dic)
        params = self._expose(params.unstack()).stack()
        predict = pd.concat(dic, axis=1).stack().reindex_like(params)
        predict[1] = 1
        predict = (predict * params).sum(axis=1, min_count=predict.shape[1]).dropna().unstack()
        dic['indust'] = predict
        fac = (mv - mv.stats.neutral(neu_axis=1, **dic).resid) / mv
        fac = self.__filter__(fac, 1)
        return fac
    
    def Fac_cashflow(self):
        shift = 4
        log = True
        periods = 4
        assets_key = 'TOT_ASSETS'
        assets = self._finance_standard(assets_key, shift, fillna=np.nan, log=log)
        mv = self._log(flow.stock('s_val_mv'))


        monetary_key = 'MONETARY_CAP'
        # 货币资金
        # 货币资金是指在企业生产经营过程中处于货币形态的那部分资金，按其形态和用途不同可分为包括库存现金、银行存款和其他货币资金。
        # 它是企业中最活跃的资金，流动性强，是企业的重要支付手段和流通手段，因而是流动资产的审查重点。
        # 货币资金：又称为货币资产，是指在企业生产经营过程中处于货币形态的资产。是指可以立即投入流通，用以购买商品或劳务或用以偿还债务的交换媒介物。
        monetary = self._finance_standard(monetary_key, shift, np.nan, log)
        monetary_gth = self._finance_gth(monetary_key, shift, np.nan, log, periods).fillna(method='ffill', limit=126)
        mon_to_assets = monetary / assets
        
        cash_end_period_key = 'CASH_CASH_EQU_END_PERIOD'
        # 期末现金及现金等价物余额
        cash_end = self._finance_standard(cash_end_period_key, shift, np.nan, log)
        cash_end_gth = self._finance_gth(cash_end_period_key, shift, np.nan, log, periods).fillna(method='ffill', limit=126)
        cash_end_to_assets = cash_end / assets
        
        cash_invin_key = 'STOT_CASH_INFLOWS_FNC_ACT'
        cash_invout_key = 'STOT_CASH_OUTFLOWS_FNC_ACT'
        cash_operin_key = 'STOT_CASH_INFLOWS_OPER_ACT'
        cash_operout_key = 'STOT_CASH_OUTFLOWS_OPER_ACT'
        cash_invin = self._finance_standard(cash_invin_key, shift, 0, log=False, quarter=True)
        cash_invout = self._finance_standard(cash_invout_key, shift, 0, log=False, quarter=True)
        cash_operin = self._finance_standard(cash_operin_key, shift, 0, log=False, quarter=True)
        cash_operout = self._finance_standard(cash_operout_key, shift, 0, log=False, quarter=True)
        cash = (cash_invin + cash_operin) / (cash_invout + cash_operout)
        cash_to_asset = ((cash_operin) / (cash_operout)) / assets
        
        dic =  {'monetary':monetary, 'monetary_gth':monetary_gth, 'mon_to_assets':mon_to_assets, 'cash_end': cash_end, 'cash_end_gth':cash_end_gth, 'cash_end_to_assets':cash_end_to_assets, 'cash':cash,'cash_to_asset':cash_to_asset}
        params = self._prem(mv, **dic)
        params = self._expose(params.unstack()).stack()
        predict = pd.concat(dic, axis=1).stack().reindex_like(params)
        predict[1] = 1
        predict = (predict * params).sum(axis=1, min_count=predict.shape[1]).dropna().unstack()
        dic['indust'] = predict
        fac = (mv - mv.stats.neutral(neu_axis=1, **dic).resid) / mv
        fac = self.__filter__(fac, 1)
        return fac
    
    def Fac_assets_liab(self):
        shift = 4
        log = True
        periods = 4
        assets_key = 'TOT_ASSETS'
        assets = self._finance_standard(assets_key, shift, fillna=np.nan, log=False)
        mv = self._log(flow.stock('s_val_mv'))
        
        liab_key = 'TOT_LIAB'
        liab = self._finance_standard(liab_key, shift, np.nan, log=False)
        liab_to_assets = liab / assets
        
        cur_liab_key = 'TOT_CUR_LIAB'
        cur_assets_key = 'TOT_CUR_ASSETS'
        cur_liab_to_assets =  self._finance_standard(cur_liab_key, shift, np.nan, log=False) /  self._finance_standard(cur_assets_key, shift, np.nan, log=False)
        
        asset_gth = self._finance_gth(assets_key, shift, np.nan, log, periods)
        assets = self._log(assets)
        dic = {'assets':assets, 'liab_to_assets':liab_to_assets, 'cur_liab_to_assets':cur_liab_to_assets, 'assets_gth':asset_gth, 'level':assets.rank(axis=1, pct=True) * asset_gth.rank(axis=1, pct=True)}
        params = self._prem(mv, **dic)
        params = self._expose(params.unstack()).stack()
        predict = pd.concat(dic, axis=1).stack().reindex_like(params)
        predict[1] = 1
        predict = (predict * params).sum(axis=1, min_count=predict.shape[1]).dropna().unstack()
        dic['indust'] = predict
        fac = (mv - mv.stats.neutral(neu_axis=1, **dic).resid) / mv
        fac = self.__filter__(fac, 1)
        return fac
        
    def Fac_operrev_cost(self):
        shift = 4
        log = True
        periods = 4
        mv = self._log(flow.stock('s_val_mv'))
        
        oper_rev_key = 'TOT_OPER_REV'
        oper_rev =  self._finance_standard(oper_rev_key, shift, np.nan, log=False, quarter=True)
        oper_cost_key = 'TOT_OPER_COST'
        oper_cost = self._finance_standard(oper_cost_key, shift, np.nan, log=False, quarter=True)
        
        cost_to_rev = oper_cost / oper_rev.replace(0, np.nan)
        
        rev_gth = self._finance_gth(oper_rev_key, shift, np.nan, log, periods, quarter=True)
        
        oper_turnover = flow.stock('INVENTORY_TURNOVER_RATIO')
        
        dic = {'oper_rev':self._log(oper_rev), 'oper_cost':self._log(oper_cost), 'cost_to_rev':cost_to_rev, 'rev_gth':rev_gth, 'oper_turnover':oper_turnover, 'level':oper_rev.rank(axis=1, pct=True) * rev_gth.rank(axis=1, pct=True)}
        params = self._prem(mv, **dic)
        params = self._expose(params.unstack()).stack()
        predict = pd.concat(dic, axis=1).stack().reindex_like(params)
        predict[1] = 1
        predict = (predict * params).sum(axis=1, min_count=predict.shape[1]).dropna().unstack()
        dic['indust'] = predict
        fac = (mv - mv.stats.neutral(neu_axis=1, **dic).resid) / mv
        fac = self.__filter__(fac, 1)
        return fac
        
    def Fac_profit(self):
        shift = 4
        log = True
        periods = 4
        mv = self._log(flow.stock('s_val_mv'))
        
        tot_profit_key = 'TOT_PROFIT'
        tot_profit =  self._finance_standard(tot_profit_key, shift, np.nan, log=False, quarter=True)
        oper_profit_key = 'OPER_PROFIT'
        oper_profit =  self._finance_standard(oper_profit_key, shift, np.nan, log=False, quarter=True)
        oper_pct = oper_profit / ((tot_profit - oper_profit).abs() + oper_profit.abs())
        oper_gth = self._finance_gth(oper_profit_key, shift, np.nan, log, periods, quarter=True)
        
        dic = {'tot_profit':self._log(tot_profit), 'oper_profit':self._log(oper_profit), 'oper_pct':oper_pct, 'oper_gth':oper_gth, 'level':oper_profit.rank(axis=1, pct=True) * oper_gth.rank(axis=1, pct=True)}
        params = self._prem(mv, **dic)
        params = self._expose(params.unstack()).stack()
        predict = pd.concat(dic, axis=1).stack().reindex_like(params)
        predict[1] = 1
        predict = (predict * params).sum(axis=1, min_count=predict.shape[1]).dropna().unstack()
        dic['indust'] = predict
        fac = (mv - mv.stats.neutral(neu_axis=1, **dic).resid) / mv
        fac = self.__filter__(fac, 1)
        return fac
    
    def Fac_gth(self):
        shift = 4
        periods = 4
        mv = self._log(flow.stock('s_val_mv'))
        
        grow_dic = {'inventory': 'INVENTORIES', 
                    'cash':'CASH_CASH_EQU_END_PERIOD', 
                    'assets': 'TOT_ASSETS', 
                    'liab': 'TOT_LIAB', 
                    'oper_rev': 'TOT_OPER_REV', 
                    'oper_cost': 'TOT_OPER_COST'}
        fac_dic = {}
        for i,j in grow_dic.items():
            df = self._finance_standard(j, shift, np.nan, False, periods=periods)   
            df = df.replace(0, np.nan)
            pct1 = df.groupby(df.index.names[0]).pct_change(fill_method=None)
            pct2 = df.groupby(df.index.names[0]).pct_change(3, fill_method=None)
            pct = pct1[pct2.index.get_level_values(1) == periods] + pct2[pct2.index.get_level_values(1) == periods]
            pct.index = pct.index.get_level_values(0)
            df = df[df.index.get_level_values(1) == periods]
            df.index = df.index.get_level_values(0)
            fac_dic[i] = self._log(df)
            fac_dic[i + '_gth'] = pct
            fac_dic[i + 'level'] = df.rank(axis=1, pct=True) * pct.rank(axis=1, pct=True)            
        params = self._prem(mv, **fac_dic)
        params = self._expose(params.unstack()).stack()
        predict = pd.concat(fac_dic, axis=1).stack().reindex_like(params)
        predict[1] = 1
        predict = (predict * params).sum(axis=1, min_count=predict.shape[1]).dropna().unstack()
        fac_dic['indust'] = predict
        fac = (mv - mv.stats.neutral(neu_axis=1, **fac_dic).resid) / mv
        fac = self.__filter__(fac, 1)
        return fac

    def abnormal1(self, df, rolling_list = [42, 63, 126]):
        pct = df
        obj = {i:{pct.index[j + i]:pct.iloc[j:j + i].cumsum() for j in range(len(pct) - i)} for i in rolling_list}
        obj = {i:{k:(l.max() - l.iloc[-1:].mean()) ** 2 - (l.min() - l.iloc[-1:].mean()) ** 2   for k,l in j.items()} for i,j in obj.items()}
        obj = {i:pd.concat(j, axis=1).T for i,j in obj.items()}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        obj.index.names = pct.index.names
        return obj
    
    @property
    def facs(self):
        if not hasattr(self, '_facs'):
            facs = {i: getattr(self, i)() for i in main.__dict__.keys() if 'Fac' in i}
            self._facs = facs
        return self._facs
        
    
    def fac_001(self):
        facs = self.facs
        test1= facs['Fac_profit'].stats.neutral(neu_axis=1, fac1 = facs['Fac_gth'], fac2=facs['Fac_inventories'], fac3=facs['Fac_cashflow'], fac4=facs['Fac_operrev_cost'], fac5=facs['Fac_assets_liab']).resid
        test2= facs['Fac_gth'].stats.neutral(neu_axis=1, fac1 = facs['Fac_profit'], fac2=facs['Fac_inventories'], fac3=facs['Fac_cashflow'], fac4=facs['Fac_operrev_cost'], fac5=facs['Fac_assets_liab']).resid
        test3= facs['Fac_inventories'].stats.neutral(neu_axis=1, fac1 = facs['Fac_profit'], fac2=facs['Fac_gth'], fac3=facs['Fac_cashflow'], fac4=facs['Fac_operrev_cost'], fac5=facs['Fac_assets_liab']).resid
        g1 = pd.concat(facs, axis=1).stack().mean(axis=1).unstack()
        g2 = g1 + (test1 + test2 - test3) / 6
        g2 = barra.barra_neutral(g2)
        return g2
    
    def fac_002(self):
        facs = {}
        for i,j in self.facs.items():
            facs[i] = self.abnormal1(j.diff())
        test1= facs['Fac_profit'].stats.neutral(neu_axis=1, fac1 = facs['Fac_gth'], fac2=facs['Fac_inventories'], fac3=facs['Fac_cashflow'], fac4=facs['Fac_operrev_cost'], fac5=facs['Fac_assets_liab']).resid
        test2= facs['Fac_gth'].stats.neutral(neu_axis=1, fac1 = facs['Fac_profit'], fac2=facs['Fac_inventories'], fac3=facs['Fac_cashflow'], fac4=facs['Fac_operrev_cost'], fac5=facs['Fac_assets_liab']).resid
        test3= facs['Fac_cashflow'].stats.neutral(neu_axis=1, fac1 = facs['Fac_profit'], fac2=facs['Fac_gth'], fac3=facs['Fac_inventories'], fac4=facs['Fac_operrev_cost'], fac5=facs['Fac_assets_liab']).resid
        g1 = pd.concat(facs, axis=1).stack().mean(axis=1).unstack()
        g2 = g1 + (test1 + test2 + test3) / 6
        g2 = barra.barra_neutral(g2)
        return g2

    



