# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 15:21:21 2021

@author: Porco Rosso
"""
import flow

from __factors__.base.main import main as meta
from __factors__.finance.config import main as config

import pandas as pd
import numpy as np

class main(meta):

    def data_init(self):
        self.initialize(**config.params)

    def TOT_OPER_REV_TTM(self):
        df = self.stock('TOT_OPER_REV_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('TOT_OPER_REV_TTM', (), {'black':black[black <= 4], 'white':white[white <= 4], 'values': obj_rank})
    
    def OPER_REV_TTM(self):
        df = self.stock('OPER_REV_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('OPER_REV_TTM', (), {'black':black[black <= 4], 'white':white[white <= 4], 'values': obj_rank})
    
    def TOT_PROFIT_TTM(self):
        df = self.stock('TOT_PROFIT_TTM')
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('TOT_PROFIT_TTM', (), {'black':black[black <= 4], 'white':white[white <= 4], 'values': obj_rank})
    
    def OPER_PROFIT_TTM(self):
        df = self.stock('OPER_PROFIT_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('OPER_PROFIT_TTM', (), {'black':black[black <= 4], 'white':white[white <= 4], 'values': obj_rank})
    
    def EBIT(self):
        df = self.stock('EBIT')
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('TOT_PROFIT_TTM', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
        
    def NET_PROFIT_TTM(self):
        df = self.stock('NET_PROFIT_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('NET_PROFIT_TTM', (), {'black':black[black <= 4], 'white':white[white <= 4], 'values': obj_rank})
    
    def PAR_COMP_NET_INC_TTM(self):
        df = self.stock('PAR_COMP_NET_INC_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('PAR_COMP_NET_INC_TTM', (), {'black':black[black <= 4], 'white':white[white <= 4], 'values': obj_rank})
    
    def OPER_REV_GROWTH_RATIO(self):
        df = self.stock('OPER_REV_GROWTH_RATIO')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = obj_rank / np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean())
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('OPER_REV_GROWTH_RATIO', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
    
    def OPER_PROFIT_GROWTH_RATIO(self):
        df = self.stock('OPER_PROFIT_GROWTH_RATIO')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = obj_rank / np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean())
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('OPER_PROFIT_GROWTH_RATIO', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
    
    def TOT_ASSET_GROWTH_RATIO(self):
        df = self.stock('TOT_ASSET_GROWTH_RATIO')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = obj_rank / np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean())
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('TOT_ASSET_GROWTH_RATIO', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
    
    def OPER_CASH_GROWTH_RATIO(self):
        df = self.stock('OPER_CASH_GROWTH_RATIO')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = obj_rank / np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean())
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('OPER_CASH_GROWTH_RATIO', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
    
    def TOT_ASSETS(self):
        df = [flow.stock('TOT_ASSETS', end=i, shift=2).iloc[-1].rename(i) for i in self.trade_days[63:]]
        df = pd.concat(df, axis=1).T        
        df.index.name = 'TRADE_DT'
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('TOT_ASSETS', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
    
    def NET_ASSETS(self):
        df = [flow.stock('TOT_ASSETS', end=i, shift=2).iloc[-1].rename(i)  - flow.stock('TOT_LIAB', end=i, shift=2).iloc[-1].rename(i)for i in self.trade_days[63:]]
        df = pd.concat(df, axis=1).T        
        df.index.name = 'TRADE_DT'
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('NET_ASSETS', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
    
    def NET_OPER_CASH_TTM(self):
        df = self.stock('NET_OPER_CASH_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('NET_OPER_CASH_TTM', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})
        
    def IM_NET_CASH_FLOWS_OPER_ACT(self):
        df = [flow.stock('IM_NET_CASH_FLOWS_OPER_ACT', end=i, shift=2).iloc[-1].rename(i) for i in self.trade_days[63:]]
        df = pd.concat(df, axis=1).T        
        df.index.name = 'TRADE_DT'
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj
        
        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = np.sign(obj_rank) * np.log(obj_rank.abs()) / np.log(np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean() + 1))
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('IM_NET_CASH_FLOWS_OPER_ACT', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})    
    
    def ROA_TTM(self):
        df = self.stock('ROA_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj

        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = obj_rank / np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean())
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('ROA_TTM', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})    
    
    def ROE_TTM(self):
        df = self.stock('ROE_TTM')    
        me = self.stock('s_val_mv')
        df_diff = df.diff().replace(0, np.nan)
        df_diff = df.diff().replace(0, np.nan)
        white = df_diff[df_diff > 0].build.event(42)
        black = df_diff[df_diff < 0].build.event(63)
        obj = df_diff.fillna(method='ffill')[white.notnull() | black.notnull()]
        add_adj = ((43 - white) / 42) ** 2
        sub_adj = ((64 - black) / 63) ** 2
        obj[obj > 0] = obj[obj > 0] * add_adj
        obj[obj < 0] = obj[obj < 0] * sub_adj

        obj_rank = pd.concat({'ind':self.stock('s_jql1_code').fillna(method='bfill'), 'market': df.add(obj.fillna(0) * 8)}, axis=1).stack()
        obj_rank = obj_rank.set_index('ind', append=True).iloc[:, 0]
        obj_rank = obj_rank / np.abs(obj_rank.groupby(['ind', 'TRADE_DT']).mean())
        obj_rank = obj_rank.reset_index('ind')['market'].unstack()
        obj_rank = obj_rank / np.log(me)
        obj_rank = obj_rank.stats.neutral(neu_axis=1, me=np.log(me)).resid
        return type('ROE_TTM', (), {'black':black[black <= 4], 'white':white[white <=4], 'values': obj_rank})    


        
