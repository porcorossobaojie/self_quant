# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:35:15 2023

@author: Porco Rosso
"""

import pandas as pd
import __pandas
import numpy as np

import requests
import pandas as pd
token = 'd7ade34c386bde324f40b234fba3ef91'
quote_url = 'https://47.252.51.154:8443/v2/usa/stock/daily_price'
index_url = 'https://47.252.51.154:8443/v2/usa/index/daily_price'
index_component_url = 'https://47.252.51.154:8443/v2/usa/index/component_stock'



class main():
    def __init__(self, filters=252*2):
        df = pd.SQL.read('join_data', 'ushareeodprices')
        df = df.drop('UNIQUE_KEY', axis=1).set_index(['TRADE_DT', 'S_INFO_WINDCODE']).unstack()
        for i in df.columns.get_level_values(0).unique():
            setattr(self, i, df[i])
        self.trade_filter = (self.S_DQ_ADJCLOSE.notnull().cumsum() > filters).fillna(False)
        self.liquird_filter = (self.S_DQ_AMOUNT.rolling(126).mean() > 10000000).fillna(False)
        lst = []
        for i in ['2018-01-01', '2018-07-01', '2019-01-01', '2019-07-01', '2020-01-01', '2020-07-01', '2021-01-01', '2021-07-01', '2022-01-01', '2022-07-01', '2023-01-01', '2023-07-01']:
            date = i
            params = {
                'token': token,
                'symbol__eq': 'SPX',
                'fields': 'stock_symbol,reject_date', # 需要用到reject日期做判断
                'select_date__lte': date,
                'select_date__order': -1,
                'size': 10000,
            }
            res = requests.get(index_component_url, params=params, verify=False)
            df = pd.DataFrame(res.json())
            df = df.drop_duplicates(subset=df.columns[0])
            obj = df[df.iloc[:, -1].isnull() | (df.iloc[:, -1] > i)].iloc[:, 0].to_frame(pd.to_datetime(i) + pd.Timedelta(15, 'h'))
            lst.append(obj)
        lst = pd.concat(lst, axis=1)
        lst = lst.stack().reset_index()
        lst.columns = ['', 'TRADE_DT', 'S_INFO_WINDCODE']
        lst = lst.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).iloc[:, 0]
        lst = lst.unstack()
        obj = lst.tools.fillna(pd.date_range(lst.index[0], pd.Timestamp.today()))
        obj = obj.notnull()
        self.spx = obj.copy().reindex_like(self.trade_filter).fillna(False)
        lst = []
        for i in ['2018-01-01', '2018-07-01', '2019-01-01', '2019-07-01', '2020-01-01', '2020-07-01', '2021-01-01', '2021-07-01', '2022-01-01', '2022-07-01', '2023-01-01', '2023-07-01']:
            date = i
            params = {
                'token': token,
                'symbol__eq': 'RUI',
                'fields': 'stock_symbol,reject_date', # 需要用到reject日期做判断
                'select_date__lte': date,
                'select_date__order': -1,
                'size': 10000,
            }
            res = requests.get(index_component_url, params=params, verify=False)
            df = pd.DataFrame(res.json())
            df = df.drop_duplicates(subset=df.columns[0])
            obj = df[df.iloc[:, -1].isnull() | (df.iloc[:, -1] > i)].iloc[:, 0].to_frame(pd.to_datetime(i) + pd.Timedelta(15, 'h'))
            lst.append(obj)
        lst = pd.concat(lst, axis=1)
        lst = lst.stack().reset_index()
        lst.columns = ['', 'TRADE_DT', 'S_INFO_WINDCODE']
        lst = lst.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).iloc[:, 0]
        lst = lst.unstack()
        obj = lst.tools.fillna(pd.date_range(lst.index[0], pd.Timestamp.today()))
        obj = obj.notnull()
        self.rui = obj.copy().reindex_like(self.trade_filter).fillna(False)

        lst = []
        for i in ['2018-01-01', '2018-07-01', '2019-01-01', '2019-07-01', '2020-01-01', '2020-07-01', '2021-01-01', '2021-07-01', '2022-01-01', '2022-07-01', '2023-01-01', '2023-07-01']:
            date = i
            params = {
                'token': token,
                'symbol__eq': 'RUT',
                'fields': 'stock_symbol,reject_date', # 需要用到reject日期做判断
                'select_date__lte': date,
                'select_date__order': -1,
                'size': 10000,
            }
            res = requests.get(index_component_url, params=params, verify=False)
            df = pd.DataFrame(res.json())
            df = df.drop_duplicates(subset=df.columns[0])
            obj = df[df.iloc[:, -1].isnull() | (df.iloc[:, -1] > i)].iloc[:, 0].to_frame(pd.to_datetime(i) + pd.Timedelta(15, 'h'))
            lst.append(obj)
        lst = pd.concat(lst, axis=1)
        lst = lst.stack().reset_index()
        lst.columns = ['', 'TRADE_DT', 'S_INFO_WINDCODE']
        lst = lst.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).iloc[:, 0]
        lst = lst.unstack()
        obj = lst.tools.fillna(pd.date_range(lst.index[0], pd.Timestamp.today()))
        obj = obj.notnull()
        self.rut = obj.copy().reindex_like(self.trade_filter).fillna(False)
        
    def __filter__(self, df, index=[ 'spx',]):
        obj = df[self.trade_filter & self.liquird_filter]
        if len(index):
            x = getattr(self, index[0])
            for i in index[1:]:
                x = x | getattr(self, i)
            obj = obj[x]
        obj = obj.dropna(how='all', axis=1)
        return obj
    
    @property
    def open(self):
        return self.__filter__(self.S_DQ_OPEN)
    
    @property
    def close(self):
        return self.__filter__(self.S_DQ_CLOSE)
    
    @property
    def low(self):
        return self.__filter__(self.S_DQ_LOW)
    
    @property
    def high(self):
        return self.__filter__(self.S_DQ_HIGH)
    
    @property
    def pct_change(self):
        if not hasattr(self, 'S_DQ_PCTCHANGE'):
            self.S_DQ_PCTCHANGE = self.S_DQ_ADJCLOSE.pct_change()
        return  self.__filter__(self.S_DQ_PCTCHANGE)
    
    @property
    def amount(self):
        return self.__filter__(self.S_DQ_AMOUNT)
    
    @property
    def volume(self):
        return self.__filter__(self.S_DQ_VOLUME)

    @property
    def turnover(self):
        return self.__filter__(self.S_DQ_TURNOVER)
    
    @property
    def adj_close(self):
        return self.__filter__(self.S_DQ_ADJCLOSE)
        
    @property
    def adj_avg(self):
        return self.__filter__(self.S_DQ_ADJAVGPRICE)
        
    def AMOUNT_STD(self, rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        amount = self.amount
        pct = self.pct_change
        obj = {i:amount.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def AMOUNT_STD_DIFF_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
        
    def AMOUNT_STD_DIFF_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def AMOUNT_STD_STD_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
        
    def AMOUNT_STD_STD_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def AMOUNT_Z(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.amount
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj
    
    def AMOUNT_Z_DIFF_1(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_Z(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj
    
    def AMOUNT_Z_DIFF_2(self, rolling_list=[10, 20, 30, 40, 50, 60], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_Z_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj
    
    def VOLUME_STD(self, rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        volume = self.volume
        pct = self.pct_change
        obj = {i:volume.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def VOLUME_STD_DIFF_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
        
    def VOLUME_STD_DIFF_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def VOLUME_STD_STD_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
        
    def VOLUME_STD_STD_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.VOLUME_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1

    def TURN_STD(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        turn = self.turnover
        pct = self.pct_change
        obj = {i:turn.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def TURN_STD_DIFF_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
        
    def TURN_STD_DIFF_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def TURN_STD_STD_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
        
    def TURN_STD_STD_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        return obj * -1
    
    def TURN_Z(self, rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.turnover
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj
    
    def TURN_Z_DIFF_1(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_Z(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj
    
    def TURN_Z_DIFF_2(self,  rolling_list=[10, 21, 42], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = self.TURN_Z_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).mean() / obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj
    
    def fac_001(self):
        am_std = pd.concat({1:self.AMOUNT_STD(neutral=False), 
                            2:self.AMOUNT_STD_DIFF_1(neutral=False), 
                            3:self.AMOUNT_STD_DIFF_2(neutral=False), 
                            4:self.AMOUNT_STD_STD_1(neutral=False), 
                            5:self.AMOUNT_STD_STD_2(neutral=False), 
                            }, axis=1).stack().mean(axis=1).unstack()
        am_z = pd.concat({1:self.AMOUNT_Z(neutral=False), 
                          2:self.AMOUNT_Z_DIFF_1(neutral=False), 
                          3:self.AMOUNT_Z_DIFF_2(neutral=False)}, axis=1).stack().mean(axis=1).unstack()
        
        tu_std = pd.concat({1:self.TURN_STD(neutral=False), 
                            2:self.TURN_STD_DIFF_1(neutral=False), 
                            3:self.TURN_STD_DIFF_2(neutral=False), 
                            4:self.TURN_STD_STD_1(neutral=False), 
                            5:self.TURN_STD_STD_2(neutral=False)}, 
                           axis=1).stack().mean(axis=1).unstack()
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

    def HIGH_TURN_CORR(self, rolling_list=[5, 10, 15, 20], neutral=False, neu_factors=None):
        high = self.high
        turn = self.turnover
        obj = pd.concat({i:high.rolling(i).corr(turn) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj * -1

    def LOW_TURN_CORR(self, rolling_list=[5, 10, 15, 20], neutral=False, neu_factors=None):
        low = self.low
        turn = self.turnover
        pct = self.pct_change
        obj = pd.concat({i:low.rolling(i).corr(turn) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj * -1
    
    def AVG_TURN_CORR(self, rolling_list=[5, 10, 15, 20], neutral=False, neu_factors=None):
        low = self.adj_avg
        turn = self.turnover
        pct = self.pct_change
        obj = pd.concat({i:low.rolling(i).corr(turn) for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj * -1
    def abnormal(self, rolling_list = [42, 63, 126], neutral=False, neu_factors=None):
        pct = self.pct_change
        obj = {i:{pct.index[j + i]:pct.iloc[j:j + i].cumsum() for j in range(len(pct) - i)} for i in rolling_list}
        obj = {i:{k:(l.max() - l.iloc[-1:].mean()) ** 2 - (l.min() - l.iloc[-1:].mean()) ** 2   for k,l in j.items()} for i,j in obj.items()}
        obj = {i:pd.concat(j, axis=1).T for i,j in obj.items()}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack()
        return obj
    
    def turns(self, rolling_list=(3,4,5)):
        pct = self.pct_change
        obj = pd.concat({i:pct.rolling(i).mean() for i in rolling_list}, axis=1)
        obj = obj[obj.abs() != np.inf]
        obj = obj.stack().mean(axis=1).unstack().stats.standard(axis=1)
        return obj * -1




self = main()
returns = self.pct_change
am_z = pd.concat({1:self.AMOUNT_Z(neutral=False), 
                  2:self.AMOUNT_Z_DIFF_1(neutral=False), 
                  3:self.AMOUNT_Z_DIFF_2(neutral=False)}, axis=1).stack().mean(axis=1).unstack()
tu_z =  pd.concat({ 1:self.TURN_Z(neutral=False), 
                    2:self.TURN_Z_DIFF_1(neutral=False), 
                    3:self.TURN_Z_DIFF_2(neutral=False)}, axis=1).stack().mean(axis=1).unstack()
vol_fac = (am_z + tu_z) / 2

high_corr = self.HIGH_TURN_CORR()
low_corr = self.LOW_TURN_CORR()
avg_corr = self.AVG_TURN_CORR()
high_low = ((high_corr + low_corr) / 2 + avg_corr) / 2
high_low = high_low#.stats.neutral(neu_axis=1, fac=np.log(self.S_DQ_CAP)).resid

turns = self.turns()

abn = self.abnormal()#.stats.neutral(neu_axis=1, fac=np.log(self.S_DQ_CAP)).resid
fac = pd.concat({'vol':vol_fac, 'high':high_low, 'turn':turns, 'abn':abn}, axis=1)
fac = fac.stack().mean(axis=1).unstack()
fac1 = fac.rolling(3).sum()
fac2 = fac.rolling(5).sum()

df1 = fac1.build.group().build.portfolio(returns).shift().loc['2020':]
df2 = fac2.build.group().build.portfolio(returns).shift().loc['2020':]

def fun(df_obj):
    df = df_obj.copy()
    df['alpha'] = df.iloc[:, -1] - df.iloc[:, 0]
    
    sharpe1 = df.analysis.sharpe(periods=len(df)).rename(('sharpe', 'total')).to_frame().T
    sharpe2 = df.resample('Y').apply(lambda x: x.analysis.sharpe())
    sharpe2.index = pd.MultiIndex.from_product([['sharpe'], sharpe2.index])
    sharpe = pd.concat([sharpe2, sharpe1])
    
    return1 = df.sum().rename(('returns', 'total')).to_frame().T
    return2 = df.resample('Y').sum()
    return2.index = pd.MultiIndex.from_product([['returns'], return2.index])
    return3 = pd.concat([return2, return1])
    
    detail1 = df.resample('Y').apply(lambda x: (x.resample('M').sum() > 0).sum() / len((x.resample('M').sum().dropna(how='all'))))
    detail1.index = pd.MultiIndex.from_product([['win month percent'], detail1.index])
    detail2 = df.resample('M').sum()
    detail2 = ((detail2 > 0).sum() / len(detail2)).to_frame(('win month percent', 'total')).T
    detail = pd.concat([detail1, detail2])
    
    volatility1 = df.std().to_frame(('volatility', 'total')).T
    volatility2 = df.resample('Y').std()
    volatility2.index = pd.MultiIndex.from_product([['volatility'], volatility2.index])
    vol = pd.concat([volatility2, volatility1])
    
    x = pd.concat([return3, vol, sharpe, detail])
    return x
    
x = fun(df2)
'''
fac = pd.concat({'me':np.log(self.__filter__(self.S_DQ_CAP)).build.group(np.linspace(0,1,5).round(2)), 'fac':fac}, axis=1)
fac.index.name = 'TRADE_DT'
fac1 = fac.stack().groupby(['TRADE_DT', 'me'])['fac'].rank(pct=True)


amz_z+ tu_z
gighcorr + howcorr logCAP
abn    logCAP

g1 = self.S_DQ_PCTCHANGE[self.spx]
g1 = g1.dropna(how='all', axis=1)
g2 = g1.sub(g1.mean(axis=1), axis=0)
g1.std(axis=1).describe()
self.spx.reindex_like
x1 = self.S_DQ_PCTCHANGE[self.rui]
x1 = x1.dropna(how='all', axis=1)
x2 = x1.sub(x1.mean(axis=1), axis=0)
x1.std(axis=1).describe()
x1 = self.S_DQ_PCTCHANGE[self.rux]
x1 = x1.dropna(how='all', axis=1)
x2 = x1.sub(x1.mean(axis=1), axis=0)
x1.std(axis=1).describe()
x1 = self.S_DQ_PCTCHANGE[self.rut]
x1 = x1.dropna(how='all', axis=1)
x2 = x1.sub(x1.mean(axis=1), axis=0)
x1.std(axis=1).describe()
'''

