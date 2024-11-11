# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:06:11 2021

@author: Porco Rosso
"""

from __factors__.base.main import main as meta
from __factors__.barra.config import main as config
import pandas as pd
import __pandas
import numpy as np
import flow

class main(meta):
    
    def data_init(self):
        self.initialize(**config.params)
        
    def lamda(self, half_life, periods, ascending=True):
        x = np.array([0.5 ** (i / half_life) for i in range(periods, 0, -1)])
        if not ascending:
            x = x[::-1]
        return x           

    def I_returns(self):
        returns = self.stock('s_dq_pctchange')
        me = self.stock('s_val_mv')
        indust = self.stock('s_jql2_code').fillna(method='bfill')
        df = pd.concat({'returns':returns, 'me':me, 'S_INFO_INDCODE': indust},axis=1).stack()
        df = df[df['returns'].notnull()]
        df['re'] = df['returns'] * df['me']
        df = df.groupby(['TRADE_DT', 'S_INFO_INDCODE'])['re', 'me'].sum()
        df = df['re'] / df['me']
        df = df.unstack()
        return df
    
    def SIZE(self):
            df = self.stock('s_val_mv')
            df = np.log(df)
            return df
    
    def I_SIZE(self):
        indust = self.stock('s_jql2_code').fillna(method='bfill')
        size = np.log(self.stock('s_val_mv'))
        df = pd.concat({'me': size, 'S_INFO_INDCODE': indust}, axis=1)
        df = df.stack().groupby(['TRADE_DT', 'S_INFO_INDCODE'])['me'].mean().unstack()
        return df  
    
    def BOOK_TO_PRICE(self):
        '''
        df = self.stock('s_dq_pb')
        df = df ** -1
        df = df.stats.neutral(neu_axis=1, me=self.SIZE()).resid
        '''
        df = [flow.stock('tot_assets', end=i, shift=2).iloc[-1].to_frame(i) for i in flow.trade_days()[252:]]
        df = pd.concat(df, axis=1).T
        mv = flow.stock('s_val_mv')
        df = df / mv / 1e8
        df = df.stats.neutral(neu_axis=1, me=self.SIZE()).resid
        #df = self.__filter__(df, self.drop_st, self.be_list_limit, self.trade_status)
        return df

    def I_BOOK_TO_PRICE(self):
        indust = self.stock('s_jql2_code').fillna(method='bfill')
        size = self.stock('s_val_mv')
        bm = self.stock('s_dq_pb') ** -1
        me = self.I_SIZE()
        df = pd.concat({'bm': bm, 'me': size, 'S_INFO_INDCODE': indust}, axis=1).stack()
        df['book_value'] = df['bm'] * df['me']
        df = df.groupby(['TRADE_DT', 'S_INFO_INDCODE'])['book_value', 'me'].sum()
        df = (df['book_value'] / df['me']).unstack()
        df = df.stats.neutral(neu_axis=1, me=me).resid
        return df
    
    def NON_LINEAR_SIZE(self):
        df = self.SIZE()
        df = (df ** 3).stats.neutral(neu_axis=1, me=df).resid.stats.standard(axis=1, rank=(-5,5))
        return df

    def I_NON_LINEAR_SIZE(self):
        df = self.I_SIZE()
        df = (df ** 3).stats.neutral(neu_axis=1, me=df).resid.stats.standard(axis=1, rank=(-5,5))
        return df

    def BETA(self):
        length = 252 # 252
        min_length = 0.67
        if not hasattr(self, '_beta'):
            mkt = self.index('s_dq_pctchange')['000905.SH']
            returns = self.stock('s_dq_pctchange')
            obj = returns.stats.neutral(neu_axis=1, me=self.SIZE(), bm=self.BOOK_TO_PRICE()).resid
            mkt = mkt.reindex(obj.index)
            lamda = self.lamda(63, length)
            if len(obj) >= length:
                beta = []
                resid = []
                for i in range(length, len(obj) + 1):
                    x = obj.iloc[i - length: i]
                    y = mkt.iloc[i - length: i]
                    xs = (x.values - x.values.mean(axis=0)) * lamda.reshape(-1,1)
                    b = np.nansum(xs * y.values.reshape(-1, 1), axis=0) / np.nansum(xs * (x.values - x.values.mean(axis=0)), axis=0)
                    r = x.sub(y.values.reshape(-1,1) * b.reshape(1, -1))
                    b = pd.Series(b, name=x.index[-1], index = x.columns)
                    b = b[x.notnull().sum() > length * min_length]
                    r = r.std().reindex(b.index).rename(x.index[-1])
                    beta.append(b)
                    resid.append(r)
                    #print(i)
                self._beta = pd.concat(beta, axis=1).T
                self._beta.index.name = returns.index.name
                self._resid = pd.concat(resid , axis=1).T
                self._resid.index.name = returns.index.name
            else:
                raise ValueError('data length must more than 252')
        #return self.__filter__(self._beta, self.drop_st, self.be_list_limit, self.trade_status)
        return self._beta
    
    def I_BETA(self):
        if not hasattr(self, '_ibeta'):
            mkt = self.index('s_dq_pctchange')['000905.SH']
            returns = self.I_returns()
            obj = returns.stats.neutral(neu_axis=1, me=self.I_SIZE(), bm=self.I_BOOK_TO_PRICE()).resid
            mkt = mkt.reindex(obj.index)
            lamda = self.lamda(63, 252)
            if len(obj) >= 252:
                beta = []
                resid = []
                for i in range(252, len(obj) + 1):
                    x = obj.iloc[i - 252: i]
                    y = mkt.iloc[i - 252: i]
                    xs = (x.values - x.values.mean(axis=0)) * lamda.reshape(-1,1)
                    b = np.nansum(xs * y.values.reshape(-1, 1), axis=0) / np.nansum(xs * (x.values - x.values.mean(axis=0)), axis=0)
                    r = x.sub(y.values.reshape(-1,1) * b.reshape(1, -1))
                    b = pd.Series(b, name=x.index[-1], index = x.columns)
                    b = b[x.notnull().sum() > 252 * 0.67]
                    r = r.std().reindex(b.index).rename(x.index[-1])
                    beta.append(b)
                    resid.append(r)
                    #print(i)
                self._ibeta = pd.concat(beta, axis=1).T
                self._ibeta.index.name = returns.index.name
                self._iresid = pd.concat(resid , axis=1).T
                self._iresid.index.name = returns.index.name
            else:
                raise ValueError('data length must more than 252')
        return self._ibeta

    def MOMENTUM(self):
        length = 504 # 504
        min_length = 0.67
        if not hasattr(self, '_momentum'):
            lamda = self.lamda(126, length)
            mkt = self.index('s_dq_pctchange')['000905.SH']
            returns = self.stock('s_dq_pctchange')
            mkt = mkt.reindex(returns.index)
            obj = returns.stats.neutral(neu_axis=1, me=self.SIZE(), bm=self.BOOK_TO_PRICE()).resid
            obj = np.log(obj+1)
            if len(obj) >= length:
                m = np.log(mkt+1).rolling(length, min_periods=int(length * min_length)).apply(lambda df: (df.mul(lamda[-1*df.shape[0]:], axis=0)).mean())
                mom = []
                for i in range(length, len(obj) + 1):
                    x = obj.iloc[i - length: i]
                    y = x.mul(lamda, axis=0).mean().rename(x.index[-1])
                    y = y[x.notnull().sum() >= int(length * min_length)]
                    mom.append(y)
                mom = pd.concat(mom, axis=1).T
                mom = mom.sub(m, axis=0).shift(21)
                mom.index.name = returns.index.name
                self._momentum = mom
            else:
                raise ValueError('data length must more than 252')
        #return self.__filter__(self._momentum, self.drop_st, self.be_list_limit, self.trade_status)
        return self._momentum
    
    def I_MOMENTUM(self):
        if not hasattr(self, '_imomentum'):
            lamda = self.lamda(126, 504)
            mkt = self.index('s_dq_pctchange')['000905.SH']
            returns = self.I_returns()
            mkt = mkt.reindex(returns.index)
            obj = returns.stats.neutral(neu_axis=1, me=self.I_SIZE(), bm=self.I_BOOK_TO_PRICE()).resid
            obj = np.log(obj+1)
            if len(obj) >= 504:
                m = np.log(mkt+1).rolling(504, min_periods=63).apply(lambda df: (df.mul(lamda[-1*df.shape[0]:], axis=0)).mean())
                mom = []
                for i in range(504, len(obj) + 1):
                    x = obj.iloc[i - 504: i]
                    y = x.mul(lamda, axis=0).mean().rename(x.index[-1])
                    y = y[x.notnull().sum() >= 21]
                    mom.append(y)
                mom = pd.concat(mom, axis=1).T
                mom = mom.sub(m, axis=0).shift(21)
                mom.index.name = returns.index.name
                self._imomentum = mom
            else:
                raise ValueError('data length must more than 252')
        return self._imomentum

    def RESIDUAL_VOLATILITY(self):
        lamda = np.expand_dims(self.lamda(42, 252), axis=1)
        returns = self.stock('s_dq_pctchange')
        mkt = self.index('s_dq_pctchange')['000905.SH'].reindex(returns.index)
        ret = returns.sub(mkt, axis=0)
        if not hasattr(self, '_res'):
            if len(ret) >= 252:
                res = []
                for i in range(252, len(ret) + 1):
                    x = ret.iloc[i - 252: i]
                    obj = np.nanmean((x.values  - x.mean().values) ** 2 * lamda, axis=0)
                    obj = pd.Series(obj, name=x.index[-1], index=x.columns)[x.notnull().sum() > (252 * 2/3)]
                    res.append(obj)
                    #print(i)
                self._res = pd.concat(res, axis=1).T
                self._res.index.name = returns.index.name
            else:
                raise ValueError('data length must more than 252')
        if not hasattr(self, '_resid'):
            self.BETA()
        res = self._res
        ret = np.log(ret + 1)
        hsigma = self._resid
        # crma = {'crma_%s' %(i): ret.rolling(i, min_periods=int(i * 2/3)).sum() for i in range(30, 361, 30)}
        # crma = pd.concat(crma, axis=1)
        # crma = crma.stack()
        # crma = np.log(crma.max(axis=1) + 1) - np.log(crma.min(axis=1) + 1)
        # crma = crma.unstack().replace(0, np.nan)
        # factor = res.stats.standard(axis=1) * 0.74 + crma.stats.standard(axis=1) * 0.16 + hsigma.stats.standard(axis=1) * 0.1
        factor = res.stats.standard(axis=1) + hsigma.stats.standard(axis=1)
        factor = factor.stats.neutral(neu_axis=1, me=self.SIZE(), beta=self.BETA()).resid
        #return self.__filter__(factor, self.drop_st, self.be_list_limit, self.trade_status)
        return factor
    
    def I_RESIDUAL_VOLATILITY(self):
        lamda = np.expand_dims(self.lamda(42, 252), axis=1)
        returns = self.I_returns()
        mkt = self.index('s_dq_pctchange')['000905.SH'].reindex(returns.index)
        ret = returns.sub(mkt, axis=0)
        if not hasattr(self, '_ires'):
            if len(ret) >= 252:
                res = []
                for i in range(252, len(ret) + 1):
                    x = ret.iloc[i - 252: i]
                    obj = np.nanmean((x.values  - x.mean().values) ** 2 * lamda, axis=0)
                    obj = pd.Series(obj, name=x.index[-1], index=x.columns)[x.notnull().sum() > 21]
                    res.append(obj)
                    #print(i)
                self._ires = pd.concat(res, axis=1).T
                self._ires.index.name = returns.index.name
            else:
                raise ValueError('data length must more than 252')
        if not hasattr(self, '_iresid'):
            self.I_BETA()
        res = self._ires
        ret = np.log(ret + 1)
        hsigma = self._iresid
        # crma = {'crma_%s' %(i): ret.rolling(i, min_periods=int(i * 2/3)).sum() for i in range(30, 361, 30)}
        # crma = pd.concat(crma, axis=1)
        # crma = crma.stack()
        # crma = np.log(crma.max(axis=1) + 1) - np.log(crma.min(axis=1) + 1)
        # crma = crma.unstack().replace(0, np.nan)
        # factor = res.stats.standard(axis=1) * 0.74 + crma.stats.standard(axis=1) * 0.16 + hsigma.stats.standard(axis=1) * 0.1
        factor = res.stats.standard(axis=1) + hsigma.stats.standard(axis=1)
        return factor

    def LIQUIDITY(self):
        df = self.stock('S_DQ_FREETURNOVER') / 100
        fac_1 = df.rolling(21, min_periods=int(21 * 2/3)).sum() + 1
        fac_2 = df.rolling(21 * 3, min_periods=int(21 * 3 * 2/3)).sum() + 1
        fac_3 = df.rolling(21 * 12, min_periods=int(21 * 12 * 2/3)).sum() + 1
        factor = np.log(fac_1) + np.log(fac_2) + np.log(fac_3)
        factor = factor.stats.neutral(neu_axis=1, me=self.SIZE(), beta=self.BETA()).resid
        #return self.__filter__(factor, self.drop_st, self.be_list_limit, self.trade_status)
        return factor
    
    def EARNING_YEILD(self):
        df = self.stock('S_DQ_PE_TTM') * 0.68 + self.stock('S_DQ_PCF_TTM') * 0.21
        df = df.stats.neutral(neu_axis=1,  me=self.SIZE(), beta=self.BETA()).resid
        #return self.__filter__(df, self.drop_st, self.be_list_limit, self.trade_status)
        return df
    
    def TURNOVER(self):
        df = self.stock('s_dq_pctchange')
        df = df.rolling(3).mean()
        return df
        
    def barra_neutral(self, df, neu_factors=None):
        if not hasattr(self, '_neu_factors'):
            self.data_init()
            factors = {'me':self.SIZE(), 'bm':self.BOOK_TO_PRICE(), 'non':self.NON_LINEAR_SIZE(), 'beta':self.BETA(), 'momentum':self.MOMENTUM(), 'earning':self.EARNING_YEILD(), 'turnover':self.TURNOVER()}
            setattr(self, '_neu_factors', factors)
        if neu_factors is None:
            neu_dic = self._neu_factors
        else:
            neu_dic = {}
            for i in neu_factors:
                if i in self._neu_factors.keys():
                    neu_dic[i] = self._neu_factors[i]
                else:
                    raise ValueError('error keys given')
        obj = df.stats.neutral(neu_axis=1, **neu_dic).resid
        return obj







