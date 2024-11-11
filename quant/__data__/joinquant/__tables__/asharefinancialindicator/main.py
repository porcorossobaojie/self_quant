# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 16:03:53 2021

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
import sys

from __data__.joinquant.__tables__.meta.meta import meta
from __data__.joinquant.__tables__.asharefinancialindicator.config import main as config

class main(meta, type('config', (), config.params)):
    @property
    def obj(self):
        if not hasattr(self, '_obj') or not hasattr(self, '_indicator'):
            date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
            date = pd.to_datetime('2010-01-01 15:00') if date is None else date
            from __data__.joinquant.__tables__.ashareeodderivativeindicator.main import main as ashareeodderivativeindicator
            indicator = ashareeodderivativeindicator().__read__(columns=['TRADE_DT', 'S_INFO_WINDCODE', 'S_VAL_MV'], where= 'TRADE_DT >= "%s"' %(date))
            indicator = indicator.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).iloc[:, 0].unstack()
            self._indicator = indicator
            date = date - pd.Timedelta( 365 * 5, 'd')
            from __data__.joinquant.__tables__.asharebalancesheet.main import main as asharebalancesheet
            balancesheet = asharebalancesheet().__read__(where= 'ANN_DT >= "%s"' %(date)).set_index(['ANN_DT', 'REPORT_PERIOD', 'S_INFO_WINDCODE']).drop('ID_KEY', axis=1)
            from __data__.joinquant.__tables__.asharecashflow.main import main as asharecashflow
            cashflow = asharecashflow().__read__(where= 'ANN_DT >= "%s"' %(date)).set_index(['ANN_DT', 'REPORT_PERIOD', 'S_INFO_WINDCODE']).drop('ID_KEY', axis=1)
            from __data__.joinquant.__tables__.ashareincome.main import main as ashareincome
            income = ashareincome().__read__(where= 'ANN_DT >= "%s"' %(date)).set_index(['ANN_DT', 'REPORT_PERIOD', 'S_INFO_WINDCODE']).drop('ID_KEY', axis=1)
            obj = pd.concat([balancesheet, cashflow, income], axis=1)
            self._obj = obj
        return self._obj
    
    @property
    def indicator(self):
        if not hasattr(self, '_indicator'):
            self.obj
        return self._indicator

    def __day_period__(self, keys, day, period, reindex=True, df=None):
        df = self.obj if df is None else df
        obj = pd.date_range(end=pd.to_datetime(day.date()), periods=period, freq='Q')
        x = df[keys][(df.index.get_level_values('ANN_DT') <= day) & (df.index.get_level_values('REPORT_PERIOD') >= obj[0])]
        x = x.unstack('S_INFO_WINDCODE').groupby('REPORT_PERIOD').sum(min_count=1)
        if reindex:
            x = x.reindex(obj)
        return x
        
    def __finance_shift__(self, df, n=2):
        bools = df.iloc[-1].isnull()
        while n > 0 and bools.any():
            n -= 1
            df.loc[:, bools] = df.loc[:, bools].shift()
            bools = df.iloc[-1].isnull()
        return df
    
    def __finance_quarter_adjust__(self, df):
        index = df.index
        tmp = df[(df.index.month == 3) & (df.index.day == 31)]
        df = df.diff()
        df.loc[tmp.index] = tmp
        df = df.reindex(index)
        return df
    
    def net_oper_cap(self, day):
        '''
        净运营资本	流动资产 - 流动负债 
        '''
        df = self.__day_period__(['TOT_CUR_ASSETS', 'TOT_CUR_LIAB'], day, 3)
        df = (df['TOT_CUR_ASSETS'] - df['TOT_CUR_LIAB'])
        df = self.__finance_shift__(df).iloc[-1].rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def tot_oper_rev_ttm(self, day):
        '''
        营业总收入TTM	计算过去12个月的 营业总收入 之和
        '''
        df = self.__day_period__('TOT_OPER_REV', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def oper_profit_ttm(self, day):
        '''
        营业利润TTM	计算过去12个月 营业利润 之和
        '''
        df = self.__day_period__('OPER_PROFIT', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df

    def net_oper_cash_ttm(self, day):
        '''
        经营活动现金流量净额TTM	计算过去12个月 经营活动产生的现金流量净值 之和
        '''
        df = self.__day_period__('NET_CASH_FLOWS_OPER_ACT', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df

    def oper_rev_ttm(self, day):
        '''
        营业收入TTM	计算过去12个月的 营业收入 之和
        '''
        df = self.__day_period__('OPER_REV', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def interest_cur_liab(self, day):
        '''
        带息流动负债	流动负债合计 - 无息流动负债
        '''
        df = self.__day_period__('TOT_CUR_LIAB', day, 3)
        df = self.__finance_shift__(df).iloc[-1]
        df = df.sub(self.interest_free_cur_liab(day), fill_value=0).replace(0, np.nan).rename(sys._getframe().f_code.co_name.upper())
        df = df.dropna()
        return df
    
    def sale_exp_ttm(self, day):
        '''
        销售费用TTM	计算过去12个月 销售费用 之和
        '''
        df = self.__day_period__('LESS_SELLING_DIST_EXP', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def retain_earn(self, day):
        '''
        留存收益	盈余公积金+未分配利润
        '''
        df = self.__day_period__(['SURPLUS_RSRV', 'UNDISTRIBUTED_PROFIT'], day, 3)
        df = df['SURPLUS_RSRV'].add(df['UNDISTRIBUTED_PROFIT'], fill_value=0).replace(0, np.nan)
        df = self.__finance_shift__(df).iloc[-1].rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def tot_oper_cost_ttm(self, day):
        '''
        营业总成本TTM	计算过去12个月的 营业总成本 之和
        '''
        df = self.__day_period__('TOT_OPER_COST', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def non_oper_net_profit_ttm(self, day):
        '''
        营业外收支净额TTM	营业外收入（TTM） - 营业外支出（TTM）
        '''
        df = self.__day_period__(['PLUS_NON_OPER_REV', 'LESS_NON_OPER_EXP'], day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = df['PLUS_NON_OPER_REV'].sub(df['LESS_NON_OPER_EXP'], fill_value=0)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df

    def net_inv_cash_ttm(self, day):
        '''
        投资活动现金流量净额TTM	计算过去12个月 投资活动现金流量净额 之和
        '''
        df = self.__day_period__('NET_CASH_FLOWS_INV_ACT', day, 7).diff()
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=1).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def fin_exp_ttm(self, day):
        '''
        财务费用TTM	计算过去12个月 财务费用 之和
        '''
        df = self.__day_period__('FIN_EXP', day, 7)
        tmp = df[(df.index.month == 6) & (df.index.day == 30)]
        df = df.diff(2)
        df.loc[tmp.index] = tmp
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=2).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def admin_exp_ttm(self, day):
        '''
        管理费用TTM	计算过去12个月 管理费用 之和
        '''
        df = self.__day_period__('LESS_GERL_ADMIN_EXP', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def net_interest_exp(self, day):
        '''
        净利息费用	利息支出-利息收入
        '''
        df = self.__day_period__(['INT_RCV','INT_PAYABLE'],  day, 3)
        df = df['INT_RCV'].sub(df['INT_PAYABLE'], fill_value=0)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=0)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def val_chg_profit_ttm(self, day):
        '''
        价值变动净收益TTM	计算过去12个月 价值变动净收益 之和
        '''
        df = self.__day_period__('PLUS_NET_GAIN_CHG_FV', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=1).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def tot_profit_ttm(self, day):
        '''
        利润总额TTM	计算过去12个月 利润总额 之和
        '''
        df = self.__day_period__('TOT_PROFIT', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def net_fin_cash_flow_ttm(self, day):
        '''
        筹资活动现金流量净额TTM	计算过去12个月 筹资活动现金流量净额 之和
        '''
        df = self.__day_period__('NET_CASH_FLOWS_FNC_ACT', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df

    def interest_free_cur_liab(self, day):
        '''
        无息流动负债	应付票据+应付账款+预收账款(用 预收款项 代替)+应交税费+应付利息+其他应付款+其他流动负债
        '''
        df = self.__day_period__(['NOTES_PAYABLE','ACCT_PAYABLE', 'ADV_FROM_CUST', 'TAXES_SURCHARGES_PAYABLE', 'INT_PAYABLE', 'OTH_PAYABLE', 'OTH_CUR_LIAB'], day, 3)
        df = df.stack().sum(min_count=1, axis=1).unstack()
        df = self.__finance_shift__(df).iloc[-1].rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def ebit(self, day):
        '''
        息税前利润	净利润+所得税+财务费用
        '''
        df = self.__day_period__(['NET_PROFIT', 'INC_TAX', 'LESS_FIN_EXP'], day, 7)
        df = df['NET_PROFIT'].add( df['INC_TAX'], fill_value=0).sub(df['LESS_FIN_EXP'], fill_value=0).replace(0, np.nan)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def net_profit_ttm(self, day):
        '''
        净利润TTM	计算过去12个月 净利润 之和
        '''
        df = self.__day_period__('NET_PROFIT', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def oper_net_inc(self, day):
        '''
        经营活动净收益	经营活动净收益/利润总额
        '''
        df = self.__day_period__(['OPER_PROFIT', 'TOT_PROFIT'], day, 7)
        df = self.__finance_quarter_adjust__(df).rolling(4, min_periods=4).sum()
        tot_profit = self.__finance_shift__(df['TOT_PROFIT']).iloc[-1]
        oper_profit = self.__finance_shift__(df['OPER_PROFIT']).iloc[-1]
        df = oper_profit.where(oper_profit > 0) / tot_profit.where(tot_profit > 0)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def asset_loss_ttm(self, day):
        '''
        资产减值损失TTM	计算过去12个月 资产减值损失 之和
        '''
        df = self.__day_period__('LESS_IMPAIR_LOSS_ASSETS', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum().rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def par_comp_net_inc_ttm(self, day):
        '''
        归属于母公司股东的净利润TTM	计算过去12个月 归属于母公司股东的净利润 之和
        '''
        df = self.__day_period__('NET_PROFIT_PARENT_COMP', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def oper_cost_ttm(self, day):
        '''
        营业成本TTM	计算过去12个月的 营业成本 之和
        '''
        df = self.__day_period__('OPER_COST', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def net_liab(self, day):
        '''
        净债务	总债务-期末现金及现金等价物余额
        '''
        df = self.__day_period__(['TOT_LIAB', 'PLUS_END_BAL_CASH_EQU'], day, 3)
        df = df['TOT_LIAB'].sub(df['PLUS_END_BAL_CASH_EQU'], fill_value=0)
        df = self.__finance_shift__(df).iloc[-1]
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df

    def net_profit_to_tot_oper_rev_ttm(self, day):
        '''
        净利润与营业总收入之比	净利润与营业总收入之比=净利润（TTM）/营业总收入（TTM）
        '''
        df = (self.net_profit_ttm(day) / self.tot_oper_rev_ttm(day).replace(0, np.nan))
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def net_profit_ratio(self, day):
        '''
        销售净利率	售净利率=净利润（TTM）/营业收入（TTM）
        '''
        df = (self.net_profit_ttm(day) / self.oper_rev_ttm(day).replace(0, np.nan))
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def net_non_oper_inc_to_tot_profit(self, day):
        '''
        营业外收支利润净额/利润总额	营业外收支利润净额/利润总额
        '''
        df = (self.non_oper_net_profit_ttm(day) / self.tot_profit_ttm(day).replace(0, np.nan))
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def degm(self, day):
        '''
        毛利率增长	毛利率增长=(今年毛利率（TTM）/去年毛利率（TTM）)-1
        考虑到负值对该因子的影响，变更为：
        毛利率增长   今年毛利（TTM） / 今年总营收（TTM） - 去年毛利（TTM） / 去年总营收（TTM）
        '''
        df = self.__day_period__(['TOT_PROFIT', 'TOT_OPER_REV'], day, 11)    
        df = self.__finance_quarter_adjust__(df)
        df = df.rolling(4, min_periods=4).sum()
        tot_profit = self.__finance_shift__(df['TOT_PROFIT'])
        tot_oper = self.__finance_shift__(df['TOT_OPER_REV'])
        x = tot_profit / tot_oper
        x = x.where(tot_oper > 0)
        x = (x.iloc[-1] - x.iloc[-5]).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return x
    
    def sale_exp_to_oper_rev(self, day):
        '''
        营业费用与营业总收入之比	营业费用与营业总收入之比=销售费用（TTM）/营业总收入（TTM）
        '''
        df = (self.sale_exp_ttm(day) / self.oper_rev_ttm(day).replace(0, np.nan))
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def net_oper_cash_ratio(self, day, fastpath=None):
        '''
        净利润现金含量	经营活动产生的现金流量净额/归属于母公司所有者的净利润
        '''
        cash = self.net_oper_cash_ttm(day)
        inc = self.par_comp_net_inc_ttm(day)
        inc = inc.where(inc > 0)
        df = cash / inc
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def intang_asset_ratio(self, day):
        '''
        无形资产比率	无形资产比率=(无形资产+研发支出+商誉)/总资产
        '''
        df = self.__day_period__(['INTANG_ASSETS', 'R_AND_D_COSTS', 'GOODWILL', 'TOT_ASSETS'], day, 3)
        df = df.stack()
        df = (df[['INTANG_ASSETS', 'R_AND_D_COSTS', 'GOODWILL']].sum(min_count=1, axis=1) / df['TOT_ASSETS']).unstack()
        df = self.__finance_shift__(df).iloc[-1]
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def inventory_turnover_ratio(self, day):
        '''
        存货周转率	存货周转率=营业成本（TTM）/存货
        '''
        oper_cost = self.__day_period__('OPER_COST', day, 7)
        inventory = self.__day_period__('INVENTORIES', day, 3)
        oper_cost = self.__finance_quarter_adjust__(oper_cost)
        oper_cost = self.__finance_shift__(oper_cost).iloc[-4:].sum(min_count=4)
        inventory = self.__finance_shift__(inventory).iloc[-1]
        df = (oper_cost / inventory.where(inventory > 0)).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def oper_profit_growth_ratio(self, day):
        '''
        营业利润增长率	营业利润增长率=(今年营业利润（TTM）/去年营业利润（TTM）)-1
        考虑到负值对该因子的影响，变更为：
        营业利润增长率   今年营业利润（TTM） / 今年营业收入（TTM） -  去年营业利润（TTM） / 去年营业收入（TTM）         
        '''
        df = self.__day_period__(['OPER_PROFIT', 'OPER_REV'], day, 11)    
        df = self.__finance_quarter_adjust__(df)
        df = df.rolling(4, min_periods=4).sum()
        profit = self.__finance_shift__(df['OPER_PROFIT'])
        rev = self.__finance_shift__(df['OPER_REV'])
        x = (profit / rev).where(df['OPER_REV'] > 0)
        x = x.iloc[-1] - x.iloc[-5]
        x = x.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return x
    
    def net_oper_cash_to_net_debt(self, day):
        '''
        经营活动产生现金流量净额/净债务	经营活动产生现金流量净额/净债务
        '''
        cash = self.net_oper_cash_ttm(day) 
        liab = self.net_liab(day)
        df = cash / liab.where(liab > 0)
        df = df.where((liab > 0) | (cash.isnull()), df.max() + 1)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def net_oper_cash_to_tot_asset(self, day):
        '''
        总资产现金回收率	经营活动产生的现金流量净额(ttm) / 总资产        
        '''
        oper_cash = self.net_oper_cash_ttm(day)
        assets = self.__day_period__('TOT_ASSETS', day, 3)
        assets = self.__finance_shift__(assets).iloc[-1].replace(0, np.nan)
        df = (oper_cash / assets).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def oper_profit_to_tot_profit(self, day):
        '''
        经营活动净收益/利润总额	经营活动净收益/利润总额        
        '''
        oper_profit = self.oper_profit_ttm(day)
        tot_profit = self.tot_profit_ttm(day)
        df = oper_profit / tot_profit.where(tot_profit > 0)
        df = df.where((tot_profit > 0) | (oper_profit.isnull()), df.min() - 1)
        df = df.rename(sys._getframe().f_code.co_name.upper())
        return df
    
    def oper_cash_to_oper_rev(self, day):
        '''
        经营活动产生的现金流量净额与营业收入之比	经营活动产生的现金流量净额（TTM） / 营业收入（TTM）
        '''
        df = self.net_oper_cash_ttm(day) / self.oper_rev_ttm(day).where(self.oper_rev_ttm(day) > 0)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df

    def roa_ttm(self, day):
        '''
        资产回报率TTM	资产回报率=净利润（TTM）/期末总资产
        期末改为期初
        '''        
        net_profit = self.net_profit_ttm(day)
        asset = self.__day_period__('TOT_ASSETS', day, 5).iloc[0].replace(0, np.nan)
        df = net_profit / asset
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def roe_ttm(self, day):
        '''
        权益回报率TTM	权益回报率=净利润（TTM）/期末股东权益
        期末改为期初
        '''        
        net_profit = self.net_profit_ttm(day)
        asset = self.__day_period__('TOT_SHRHLDR_EQY_INCL_MIN_INT', day, 5).iloc[0]
        asset = asset.where(asset > 0)
        df = net_profit / asset
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def oper_rev_growth_ratio(self, day):
        '''
        营业收入增长率	营业收入增长率=（今年营业收入（TTM）/去年营业收入（TTM））-1
        '''
        df = self.__day_period__('OPER_REV', day, 11)
        df = self.__finance_quarter_adjust__(df)
        df = df.rolling(4, min_periods=4).sum()
        df = self.__finance_shift__(df)
        x = df.iloc[-1] / df.iloc[-5].where(df.iloc[-5] > 0)
        x = x.where((df.iloc[-5] > 0) | (df.iloc[-1] > 0) | (df.iloc[[-1, -5]].isnull().any()), x.min() - 1) - 1
        x = x.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return x
    
    def tot_asset_growth_ratio(self, day):
        '''
        总资产增长率	总资产 / 总资产_4 -1
        '''
        df = self.__day_period__('TOT_ASSETS', day, 7)
        df = self.__finance_shift__(df)
        df = (df.iloc[-1] / df.iloc[-5].where(df.iloc[-5] > 0) - 1).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def oper_cash_growth_ratio(self, day):
        '''
        经营活动产生的现金流量净额增长率	(今年经营活动产生的现金流量净额（TTM）/去年经营活动产生的现金流量净额（TTM）)-1
        '''
        df = self.__day_period__('NET_CASH_FLOWS_OPER_ACT', day, 11)
        df = self.__finance_quarter_adjust__(df).rolling(4, min_periods=4).sum()
        df = self.__finance_shift__(df)
        x = df.iloc[-1] / df.iloc[-5].where(df.iloc[-5] > 0)
        x = x.where((df.iloc[-5] > 0) | (df.iloc[-1] > 0) | (df.iloc[[-1, -5]].isnull().any()), x.min() - 1) - 1
        x = x.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return x
    
    def tot_oper_rev_ttm_to_mkt(self, day):
        '''
        每股营业总收入TTM	营业总收入（TTM）除以总股本
        更改： 总股本变更为总市值
        '''
        df = self.tot_oper_rev_ttm(day) / (self.indicator.loc[:day].iloc[-1] * 10e8)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def cash_equity_to_mkt(self, day):
        '''
        每股现金及现金等价物余额	每股现金及现金等价物余额
        更改： 总股本变更为总市值
        '''
        df = self.__day_period__('CASH_CASH_EQU_END_PERIOD', day, 3)
        df = self.__finance_shift__(df).iloc[-1]
        df = (df / (self.indicator.loc[:day].iloc[-1] * 10e8)).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def oper_rev_ttm_to_mkt(self, day):
        '''
        每股营业收入TTM	营业收入（TTM）除以总股本
        更改： 总股本变更为总市值
        '''
        df = self.oper_rev_ttm(day) / (self.indicator.loc[:day].iloc[-1] * 10e8)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def net_asset_to_mkt(self, day):
        '''
        每股净资产	归属母公司所有者权益合计除以总股本
        更改： 总股本变更为总市值
        '''
        df = self.__day_period__('TOT_SHRHLDR_EQY_INCL_MIN_INT', day, 3)
        df = self.__finance_shift__(df).iloc[-1]
        df = (df / (self.indicator.loc[:day].iloc[-1] * 10e8)).rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def oper_cash_ttm_to_mkt(self, day):
        '''
        每股经营活动产生的现金流量净额	每股经营活动产生的现金流量净额
        更改： 总股本变更为总市值
        '''
        df = self.net_oper_cash_ttm(day) / (self.indicator.loc[:day].iloc[-1] * 10e8)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
        
    def oper_profit_ttm_to_mkt(self, day):
        '''
        每股营业利润TTM	营业利润（TTM）除以总股本
        更改： 总股本变更为总市值
        '''
        df = self.oper_profit_ttm(day) / (self.indicator.loc[:day].iloc[-1] * 10e8)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
    
    def eps_ttm(self, day):
        '''
        每股收益TTM	过去12个月归属母公司所有者的净利润（TTM）除以总股本
        更改： 总股本变更为总市值
        '''
        df = self.__day_period__('NET_PROFIT_PARENT_COMP', day, 7)
        df = self.__finance_quarter_adjust__(df)
        df = self.__finance_shift__(df).iloc[-4:].sum(min_count=4)
        df = df / (self.indicator.loc[:day].iloc[-1] * 10e8)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
         
    def cash_ttm_to_mkt(self, day):
        '''
        每股现金流量净额，根据当时日期来获取最近变更日的总股本	现金流量净额（TTM）除以总股本
        更改： 总股本变更为总市值
        '''
        df = self.__day_period__('END_BAL_CASH', day, 7)
        df = self.__finance_shift__(df)
        df = df.iloc[-1] - df.iloc[-5]
        df = df / (self.indicator.loc[:day].iloc[-1] * 10e8)
        df = df.rename(sys._getframe().f_code.co_name.upper()).dropna()
        return df
                
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True, columns={i.upper():j for i,j in self.columns.items()})
        date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
        date = pd.to_datetime('2005-01-01') if date is None else date
        periods = self.__days__(max(date, pd.to_datetime('2010-01-01 15:00')))
        funcs = [getattr(self, i, None) for i in self.columns.keys()]
        if len(periods):
            for i in periods:
                if i in self.trade_days:
                    try:
                        print(i)
                        lst = [func(i) for func in funcs if func is not None]
                        lst = pd.concat(lst, axis=1).reset_index()
                        lst['TRADE_DT'] = i
                        self.__write__(lst.reindex([i.upper() for i in self.columns.keys()], axis=1))
                    except:
                        pass
                    
                    
                    
'''
helps = pd.SQL.login.__schemas_info__(where = 'TABLE_SCHEMA = "join_data"')[['TABLE_SCHEMA', 'TABLE_NAME', 'COLUMN_NAME', 'COLUMN_COMMENT']]
helps[['COMMENT', 'DETAIL']] = helps['COLUMN_COMMENT'].str.split('\n', expand=True).fillna('')
'''

















