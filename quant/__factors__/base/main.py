# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 09:56:20 2021

@author: Porco Rosso
"""

import sys

import flow
from __factors__.base.config import main as config

class main(type('filter_rule', (), {'%s' %(i): j for i, j in config.filter_rule.items()})):

    table_infomation = config.table_infomation
    flow = flow
    
    @classmethod
    def __source__(cls, table=None, key_list=None):
        key_list = cls.table_infomation[table] if key_list is None else key_list
        flow.stock(key_list)
            
    @classmethod
    def initialize(cls, **kwargs):
        if len(kwargs):
            [flow.stock(i) for i in kwargs.values()]
        else:
            [cls.__source__(i) for i in cls.table_infomation.keys()]
            
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items()]
        if self.begin is not None:
            flow.initialize(self.begin)
            
    def __filter__(self, df, drop_st=None, be_list=None, trade_status=None):
        drop_st = self.drop_st if drop_st is None else drop_st
        be_list = self.be_list_limit if be_list is None else be_list
        trade_status = self.trade_status if trade_status is None else trade_status
        if drop_st:
            df = df[(flow.is_st() < drop_st).reindex_like(df).fillna(False)]
        if be_list:
            df = df[flow.be_list(be_list).reindex_like(df)]
        if trade_status:
            df = df[flow.stock('s_dq_tradestatus').reindex_like(df).fillna(0).astype(bool)]
        return df
    
    @property
    def trade_days(self):
        if not hasattr(self, '_trade_days'):
            setattr(self, '_trade_days', flow.trade_days())
        return self._trade_days
                
    def stock(self, key, drop_st=None, be_list=None, trade_status=None, **kwargs):
        drop_st = self.drop_st if drop_st is None else drop_st
        be_list = self.be_list_limit if be_list is None else be_list
        trade_status = self.trade_status if trade_status is None else trade_status
        df = flow.stock(key, **kwargs)
        #return self.__filter__(df, drop_st, be_list, trade_status)
        return df
    
    def index(self, key):
        return flow.index(key)

        
    
        









