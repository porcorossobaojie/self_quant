# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 16:50:21 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.meta.meta import meta, jq
from __data__.joinquant.__tables__.ashareeomprices.config import main as config

import pandas as pd
import numpy as np

class main(meta, type('config', (), config.params)):
    trade_days = pd.to_datetime(jq.get_trade_days('2017-01-01')) + pd.Timedelta(15, 'h')
    def __source__(self, date=None):
        if date == self.trade_days[0]:
            obj = pd.DataFrame(columns=self.columns.keys())
            return obj
    
        df = pd.SQL.read(schemas='join_data', table='ashareeodprices1min', where="TRADE_DT >= '%s' and TRADE_DT <= '%s'" %(date.date(), date))
        if df.shape[0]:
            me = pd.SQL.read(schemas='join_data', table='ashareeodderivativeindicator', where="TRADE_DT= '%s'" %(self.trade_days[self.trade_days.get_loc(date) - 1])).set_index('S_INFO_WINDCODE')['S_VAL_MV']
            df = df.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).unstack()
            pct_change = df['S_MQ_PCTCHANGE']
            amount = df['S_MQ_AMOUNT'] / 1000000
            turnover = amount / me 

            pct_diff = pct_change.sub((pct_change * amount).sum() / amount.sum())
            turn_diff = turnover.sub(turnover.mean(axis=1), axis=0)

            pct_sign = (np.sign(pct_change) * turnover).sum()
            pd_sign = (np.sign(pct_diff) * turnover).sum()
            pct_corr = pct_change.corrwith(turnover)
            pd_corr = pct_diff.corrwith(turn_diff)
            putu = (turn_diff[turn_diff >= 0] * pct_diff[pct_diff >=0]).sum(min_count=1)
            pdtu = (turn_diff[turn_diff >= 0] * pct_diff[pct_diff < 0]).sum(min_count=1) * -1
            pdtd = (turn_diff[turn_diff < 0] * pct_diff[pct_diff < 0]).sum(min_count=1)
            putd = (turn_diff[turn_diff < 0] * pct_diff[pct_diff >= 0]).sum(min_count=1) * -1
            turn_std = turnover.std()
            tudf_std = turn_diff.std()
            
            obj1 = pd.concat([pct_sign, pd_sign, pct_corr, pd_corr, putu, pdtu, pdtd, putd, turn_std, tudf_std], axis=1)
            obj1.columns = ['PCT_SIGN_TURN', 'PCTDIFF_SIGN_TURN', 'PCT_CORR', 'PCTDIFF_CORR', 'PUTU', 'PDTU', 'PDTD', 'PUTD', 'TURN_STD', 'TUDF_STD']
                        
            # high/low pctchange adjust
            is_high_limit = (df['S_MQ_CLOSE'] >= df['S_MQ_HIGH_LIMIT'] - 0.01)
            is_low_limit = (df['S_MQ_CLOSE'] <= df['S_MQ_LOW_LIMIT'] + 0.01)

            pct_change = pct_change[~((pct_change == 0) & (is_high_limit | is_low_limit))]            
            pct_change = pct_change.fillna(pct_change.fillna(0).ewm(alpha=0.5).mean())
            turnover = turnover[~((turnover == 0) & (is_high_limit | is_low_limit)).astype(bool)]
            turnover = turnover.fillna(turnover.fillna(0).ewm(alpha=0.5).mean())
            
            pct_diff = pct_change.sub((pct_change * amount).sum() / amount.sum())
            turn_diff = turnover.sub(turnover.mean(axis=1), axis=0)
            
            pct_sign = (np.sign(pct_change) * turnover).sum()
            pd_sign = (np.sign(pct_diff) * turnover).sum()
            pct_corr = pct_change.corrwith(turnover.replace(0, np.nan))
            pd_corr = pct_diff.corrwith(turn_diff.replace(0, np.nan))
            putu = (turn_diff[turn_diff >= 0] * pct_diff[pct_diff >=0]).sum(min_count=1)
            pdtu = (turn_diff[turn_diff >= 0] * pct_diff[pct_diff < 0]).sum(min_count=1) * -1
            pdtd = (turn_diff[turn_diff < 0] * pct_diff[pct_diff < 0]).sum(min_count=1)
            putd = (turn_diff[turn_diff < 0] * pct_diff[pct_diff >= 0]).sum(min_count=1) * -1
            turn_std = turnover.std()
            tudf_std = turn_diff.std()
            
            obj2 = pd.concat([pct_sign, pd_sign, pct_corr, pd_corr, putu, pdtu, pdtd, putd, turn_std, tudf_std], axis=1)
            obj2.columns = obj1.columns + '_ADJ'
            
            obj = pd.concat([obj1, obj2], axis=1).reset_index()
            obj['TRADE_DT'] = date
        else:
            obj = pd.DataFrame(columns=self.columns.keys())
        return obj
    
    def daily(self, exist='append'):
        if self.__exist__() and exist == 'replace' or not self.__exist__():
            self.__command__('DROP TABLE IF EXISTS %s' %(self.table))
            self.__create__(log=True)
        date = self.__command__('SELECT MAX(TRADE_DT) FROM %s' %(self.table))[0][0]
        periods = self.__days__(date)
        if len(periods):
            for i in periods:
                if i in self.trade_days:
                    print(i)
                    df = self.__source__(i)
                    self.__write__(df)
                
            
        
'''
PCT_CORR: 0.1
PCTDIFF_SIGN_TURN: 0.1 0.9
PUTU 0.8
PDTU 0.8
PDTD 0.1
PUTD 0.9
TURN_STD 0.8
TUDF_STD 0.8
PCT_SIGN_TURN_ADJ 0.1
PCTDIFF_SIGN_TURN_ADJ 0.1
PCT_CORR_ADJ 0.1
PUTU_ADJ 0.8
PDTD_ADJ 0.1
PUTD_ADJ 0.1 0.9
TURN_STD_ADJ 0.8
TUDF_STD_ADJ 0.8

dic = {}
for i in ['PCT_CORR', 'PCTDIFF_SIGN_TURN', 'PUTU', 'PDTU', 'PDTD', 'PUTD', 'TURN_STD', 'TUDF_STD', 'PCT_SIGN_TURN_ADJ', 'PCT_CORR_ADJ', 'PUTU_ADJ', 'PDTD_ADJ', 'PUTD_ADJ','TURN_STD_ADJ','TUDF_STD_ADJ']:
    dic[i] = x1[i].rank(axis=1, pct=True).stack()

dic['PCT_CORR'] = dic['PCT_CORR'] < 0.05
dic['PCTDIFF_SIGN_TURN'] = (dic['PCTDIFF_SIGN_TURN'] < 0.05) | (dic['PCTDIFF_SIGN_TURN'] > 0.95)
dic['PUTU'] = dic['PUTU'] > 0.05
dic['PDTU'] = dic['PDTU'] > 0.95
dic['PDTD'] = dic['PDTD'] < 0.05
dic['PUTD'] = dic['PUTD'] > 0.95
dic['TURN_STD'] = dic['TURN_STD'] > 0.95
dic['TUDF_STD'] = dic['TUDF_STD'] > 0.95
dic['PCT_SIGN_TURN_ADJ'] = dic['PCT_SIGN_TURN_ADJ'] < 0.05
dic['PCT_CORR_ADJ'] = dic['PCT_CORR_ADJ'] < 0.05
dic['PUTU_ADJ'] = dic['PUTU_ADJ'] > 0.95
dic['PDTD_ADJ'] = dic['PDTD_ADJ'] < 0.05
dic['PUTD_ADJ'] = (dic['PUTD_ADJ'] < 0.05) | (dic['PUTD_ADJ'] > 0.95)
dic['TURN_STD_ADJ'] = dic['TURN_STD_ADJ'] > 0.95
dic['TUDF_STD_ADJ'] = dic['TUDF_STD_ADJ'] > 0.95





'''



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
