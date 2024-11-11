# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 20:00:11 2022

@author: Porco Rosso
"""

from __factors__.base.main import main as meta
from __factors__ import barra
from __factors__.market.config import main as config

import pandas as pd
import __pandas
import numpy as np
import flow

class main(meta):

    def data_init(self):
        self.initialize(**config.params)

    @property
    def open(self):
        return self.stock('s_dq_open')
    
    @property
    def close(self):
        return self.stock('s_dq_close')
    
    @property
    def low(self):
        return self.stock('s_dq_low')
    
    @property
    def high(self):
        return self.stock('s_dq_high')
    
    @property
    def avg(self):
        return self.stock('s_dq_avgprice')
    
    @property
    def pct_change(self):
        return self.stock('s_dq_pctchange')
    
    @property
    def amount(self):
        return self.stock('s_dq_amount')
    
    @property
    def volume(self):
        return self.stock('s_dq_volume')

    @property
    def turnover(self, adj=False):
        if adj:
            if not hasattr(self, '_turnover'):
                df = pd.concat([flow.stock(['s_jql1_code', 's_swl1_code']), flow.stock(['s_dq_freeturnover'])], axis=1)
                df = df.stack().set_index(['S_JQL1_CODE', 'S_SWL1_CODE'], append=True)
                df = df * 2 - df.groupby(['TRADE_DT', 'S_JQL1_CODE']).transform('mean') -  df.groupby(['TRADE_DT', 'S_SWL1_CODE']).transform('mean')
                df = df.reset_index(['S_JQL1_CODE', 'S_SWL1_CODE'])['S_DQ_FREETURNOVER'].unstack()
                self._turnover = df
            df = self._turnover
            return self._turnover
        else:
            return self.stock('s_dq_freeturnover')
    
    @property
    def adj_close(self):
        return self.stock('s_dq_adjclose')
        
    @property
    def adj_avg(self):
        return self.stock('s_dq_adjavgprice')

    # amount / free turnover / volume in Voltility
    def AMOUNT_STD(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        amount = self.amount
        pct = self.pct_change
        obj = {i:amount.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def AMOUNT_STD_DIFF_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def AMOUNT_STD_DIFF_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def AMOUNT_STD_STD_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def AMOUNT_STD_STD_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def AMOUNT_Z(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.amount
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def AMOUNT_Z_DIFF_1(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_Z(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def AMOUNT_Z_DIFF_2(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_Z_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj

    def VOLUME_STD(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        volume = self.volume
        pct = self.pct_change
        obj = {i:volume.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def VOLUME_STD_DIFF_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def VOLUME_STD_DIFF_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def VOLUME_STD_STD_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def VOLUME_STD_STD_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1

    def TURN_STD(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        turn = self.turnover
        pct = self.pct_change
        obj = {i:turn.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def TURN_STD_DIFF_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def TURN_STD_DIFF_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def TURN_STD_STD_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def TURN_STD_STD_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def TURN_Z(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.turnover
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def TURN_Z_DIFF_1(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_Z(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def TURN_Z_DIFF_2(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_Z_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def fac_001(self):
        am_std = pd.concat({1:self.AMOUNT_STD(neutral=False), 
                            2:self.AMOUNT_STD_DIFF_1(neutral=False), 
                            3:self.AMOUNT_STD_DIFF_2(neutral=False), 
                            4:self.AMOUNT_STD_STD_1(neutral=False), 
                            5:self.AMOUNT_STD_STD_2(neutral=False), 
                            }, axis=1).stack().mean(axis=1).unstack()
        am_std = barra.barra_neutral(am_std)
        am_z = pd.concat({1:self.AMOUNT_Z(neutral=False), 
                          2:self.AMOUNT_Z_DIFF_1(neutral=False), 
                          3:self.AMOUNT_Z_DIFF_2(neutral=False)}, axis=1).stack().mean(axis=1).unstack()
        am_z = barra.barra_neutral(am_z)
        
        tu_std = pd.concat({1:self.TURN_STD(neutral=False), 
                            2:self.TURN_STD_DIFF_1(neutral=False), 
                            3:self.TURN_STD_DIFF_2(neutral=False), 
                            4:self.TURN_STD_STD_1(neutral=False), 
                            5:self.TURN_STD_STD_2(neutral=False)}, 
                           axis=1).stack().mean(axis=1).unstack()
        tu_std = barra.barra_neutral(tu_std)
        '''
        tu_z =  pd.concat({ 1:self.TURN_Z(neutral=False), 
                            2:self.TURN_Z_DIFF_1(neutral=False), 
                            3:self.TURN_Z_DIFF_2(neutral=False)}, axis=1).stack().mean(axis=1).unstack()
        tu_z = barra.barra_neutral(tu_z)
        
        pri_std = pd.concat({1:self.PRICE_STD(neutral=False),
                            2:self.PRICE_STD_DIFF_1(neutral=False), 
                            3:self.PRICE_STD_DIFF_2(neutral=False), 
                            4:self.PRICE_STD_STD_1(neutral=False), 
                            5:self.PRICE_STD_STD_2(neutral=False)}, 
                           axis=1).stack().mean(axis=1).unstack()
        pri_std = barra.barra_neutral(pri_std)
        '''
        '''
        fac's self corr too low at 0.9
        x = pd.concat({'am_std':am_std.stats.standard(axis=1), 'am_z':am_z.stats.standard(axis=1), 'tu_std':tu_std.stats.standard(axis=1), 'tu_z':tu_z.stats.standard(axis=1), 'pri_std':pri_std.stats.standard(axis=1)}, axis=1).stack()
        x = np.exp(x) / (1 + np.exp(x))
        weight = np.array([0.2, 4.0, 3.55, 0.65, 0.15]).repeat(len(x)).reshape(5, -1).T
        weight = pd.DataFrame(weight, index=x.index, columns=x.columns)
        weight = weight[x.sub(x.mean(axis=1), axis=0).abs().sub(x.sub(x.mean(axis=1), axis=0).abs().max(axis=1), axis=0) < 0]
        fac = ((x * weight).sum(axis=1) / weight.sum(axis=1)).unstack()
        '''
        
        x = pd.concat({'am_std':am_std*0.8, 'am_z':am_z*1, 'tu_std':tu_std * 2.5, }, axis=1).stack().mean(axis=1).unstack()
        return x

    def am_std(self):
        am_std1 = pd.concat({1:self.AMOUNT_STD(neutral=False), 
                            2:self.AMOUNT_STD_DIFF_1(neutral=False), 
                            3:self.AMOUNT_STD_DIFF_2(neutral=False), 
                            }, axis=1).stack()
        am_std1 = am_std1[am_std1.sub(am_std1.max(axis=1), axis=0) < 0].mean(axis=1).unstack()
        am_std2 = pd.concat({4:self.AMOUNT_STD_STD_1(neutral=False), 
                             5:self.AMOUNT_STD_STD_2(neutral=False)}, axis=1).stack().min(axis=1).unstack()
        am_std = barra.barra_neutral(am_std1 + am_std2, neu_factors=['me', 'beta', 'momentum', 'non', 'earning', 'bm'])
        return am_std
    
    def am_z(self):
        am_z = pd.concat({1:self.AMOUNT_Z(neutral=False), 
                          2:self.AMOUNT_Z_DIFF_1(neutral=False), 
                          3:self.AMOUNT_Z_DIFF_2(neutral=False)}, axis=1).stack().mean(axis=1).unstack()
        #am_z = am_z[am_z.sub(am_z.max(axis=1), axis=0) < 0].mean(axis=1).unstack()
        am_z = barra.barra_neutral(am_z)
        return am_z
    
    def tu_std(self):
        tu_std = pd.concat({1:self.TURN_STD(neutral=False), 
                            2:self.TURN_STD_DIFF_1(neutral=False), 
                            3:self.TURN_STD_DIFF_2(neutral=False),
                            4:self.TURN_STD_STD_1(neutral=False), 
                            5:self.TURN_STD_STD_2(neutral=False)}, 
                           axis=1).stack()
        tu_std = tu_std[tu_std.sub(tu_std.max(axis=1), axis=0) < 0].mean(axis=1).unstack()
        tu_std = barra.barra_neutral(tu_std, neu_factors=['me', 'beta', 'momentum', 'non', 'earning', 'bm'])
        
    def fun(self):
        import flow
        g1 = (flow.stock('s_dq_freeturnover') * flow.stock('s_dq_mv').shift(21)).rolling(21).sum()           
        g2 = flow.stock('s_dq_mv').rolling(21).sum()
        g3 = g1 / g2
        g4 = g3.rolling(126).rank(pct=True)
        
    # returns in voltility
    # useless
    def PCT_STD(self, rolling_list=[40, 50, 60, 70, 80, 90], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = pct
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def PCT_STD_DIFF_1(self, rolling_list=[40, 50, 60, 70, 80, 90], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PCT_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def PCT_STD_DIFF_2(self, rolling_list=[40, 50, 60, 70, 80, 90], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PCT_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def PCT_STD_STD_1(self, rolling_list=[40, 50, 60, 70, 80, 90], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PCT_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def PCT_STD_STD_2(self, rolling_list=[40, 50, 60, 70, 80, 90], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PCT_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def PCT_Z(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = pct
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def PCT_Z_DIFF_1(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PCT_Z(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    def PCT_Z_DIFF_2(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PCT_Z_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj
    
    # voltility in daily
    def PRICE_STD(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        open = self.open
        close = self.close
        adj_close = self.adj_close
        high = self.high
        low = self.low
        x1 = open / close.shift()
        x2 = adj_close / adj_close.shift()
        x3 = high / close.shift()
        x4 = low / close.shift()
        x5 = (high - low) / close.shift()
        x6 = open / close
        
        obj = pd.concat({5:x5*2, 6:(x6 - 1) *1}, axis=1)
        obj = (obj ** 2).stack().mean(axis=1).unstack()
        obj = pd.concat({i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1
    
    def PRICE_STD_DIFF_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PRICE_STD(rolling_list, neutral, neu_factors).diff()
        obj = pd.concat({i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1

    def PRICE_STD_DIFF_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PRICE_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = pd.concat({i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1
    
    def PRICE_STD_STD_1(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PRICE_STD(rolling_list, neutral, neu_factors)
        obj = pd.concat({i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1

    def PRICE_STD_STD_2(self, rolling_list=[42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.PRICE_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = pd.concat({i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1

    def PRICE_Z(self, rolling_list=[42, 52, 63, 73, 84], neutral=False, neu_factors=None):
        pct = self.pct_change
        open = self.open
        close = self.close
        adj_close = self.adj_close
        high = self.high
        low = self.low
        x1 = open / close.shift()
        x2 = adj_close / adj_close.shift()
        x3 = high / close.shift()
        x4 = low / close.shift()
        x5 = (high - low) / close.shift()
        x6 = open / close
        obj = pd.concat({5:x5*2, 6:(x6 - 1) *1}, axis=1)
        obj = (obj ** 2).stack().mean(axis=1).unstack()
        x = pd.concat({i:obj.rolling(i).mean() / obj.rolling(i).std() for i in rolling_list}, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        x = x.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            x = barra.barra_neutral(x, neu_factors)        
        return x * -1

    def HIGH_TURN_CORR(self, rolling_list=[5, 10, 15, 20], neutral=False, neu_factors=None):
        high = self.high
        turn = self.turnover
        pct = self.pct_change
        obj = pd.concat({i:high.rolling(i).corr(turn) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1
    
    def LOW_TURN_CORR(self, rolling_list=[5, 10, 15, 20], neutral=False, neu_factors=None):
        low = self.low
        turn = self.turnover
        pct = self.pct_change
        obj = pd.concat({i:low.rolling(i).corr(turn) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1
    
    def HIGH_LOW_DIFF(self, rolling_list=[5, 10, 15, 20], neutral=False, neu_factors=None):
        low = self.low
        high = self.high
        x = high / low
        turn = self.turnover
        pct = self.pct_change
        obj = pd.concat({i:x.rolling(i).corr(turn) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)        
        return obj * -1    
        
    def sw_001(self, rolling_list=[4,5,6,7,8,9,10], neutral=False, neu_factors=None):
        pct = self.pct_change
        volume = self.volume
        open = self.open
        close = self.close
        obj = pd.concat({i:((open - close.shift()) / close.shift()).rank(axis=1, pct=True).rolling(i).corr(np.log(volume).diff().rank(axis=1, pct=True)) - ((open - close) / close).rank(axis=1, pct=True).rolling(i).corr(np.log(volume).diff().rank(axis=1, pct=True)) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        x = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid * -1
        if neutral:
            x = barra.barra_neutral(x, neu_factors)        
        return x
        
    def abnormal1(self, rolling_list = [42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = {i:{pct.index[j + i]:pct.iloc[j:j + i].cumsum() for j in range(len(pct) - i)} for i in rolling_list}
        obj = {i:{k:(l.max() - l.iloc[-1:].mean()) ** 2 - (l.min() - l.iloc[-1:].mean()) ** 2   for k,l in j.items()} for i,j in obj.items()}
        obj = {i:pd.concat(j, axis=1).T for i,j in obj.items()}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        obj.index.names = pct.index.names
        x = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid 
        if neutral:
            x = barra.barra_neutral(x, neu_factors)        
        return x
        
    def abnormal2(self, rolling_list = [5, 10], neutral=False, neu_factors=None):
        amount = self.amount * 0.5
        netmain = self.stock('s_dq_netmain') * 10000 
        pct = self.pct_change
        
        obj = {i:(amount + netmain).rolling(i).mean() / (amount - netmain).rolling(i).mean()  for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        x = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid 
        if neutral:
            x = barra.barra_neutral(x, neu_factors)        
        return x
    
    def tr1(self, rolling_list = [42, 63, 126], neutral=False, neu_factors=None):
        adj = self.stock('s_dq_post_factor')
        high = self.high * adj
        low = self.low * adj
        close = self.close * adj
        pct = self.pct_change
        fac = pd.concat({0:(high - low), 1:(high - close.shift()), 2:(low - close.shift())}, axis=1)
        fac = fac.abs().stack().max(axis=1).unstack()
        fac = fac / close.shift()
        obj = {i:((fac.rolling(i).mean().shift() - fac) * pct).ewm(halflife=i, ignore_na=True, min_periods=i).mean() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        x = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid 
        if neutral:
            x = barra.barra_neutral(x, neu_factors)        
        return x
    
    def tr2(self, rolling_list = [42, 63, 126], neutral=False, neu_factors=None):
        turnover = self.turnover
        pct = self.pct_change
        fac = turnover
        obj = {i:((fac.rolling(i).mean().shift() - fac) * pct).ewm(halflife=i, ignore_na=True, min_periods=i).mean() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        x1 = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid 

