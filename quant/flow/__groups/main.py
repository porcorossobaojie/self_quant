# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:11:16 2021

@author: Porco Rosso
"""

from flow.__tables.main import ashareeodprices, ashareeodprices1min, ashareeodderivativeindicator, asharebalancesheet, asharecashflow, ashareincome, asharefinancialindicator, aindexeodprices, ashareindustriesclass, ashareorder, ashareconnect, ashareperformanceletter 
from flow.__groups.meta import meta

import pandas as pd
import __pandas

class stock(meta):
    __tables__ = [ashareeodprices, ashareeodprices1min, ashareeodderivativeindicator, asharebalancesheet, asharecashflow, ashareincome, asharefinancialindicator, ashareindustriesclass, ashareorder, ashareconnect, ashareperformanceletter]
    __schemas__ = list(set(['"%s"' %(i.schemas) for i in __tables__]))
    __schemas__ = ('TABLE_SCHEMA = %s' %(__schemas__[0])) if len(__schemas__) == 1 else 'TABLE_SCHEMA IN (%s)' %(','.join(__schemas__))
    __table_name__ = 'TABLE_NAME IN (%s)' %(','.join(['"%s"' %(i.__name__) for i in __tables__]))
    _help = pd.SQL.info(columns = ['TABLE_SCHEMA' ,'TABLE_NAME', 'COLUMN_NAME', 'COLUMN_COMMENT'], where = ' AND '.join([__schemas__, __table_name__]))
    
    @property
    def days(self):
        if not len(self.ashareeodprices.values.index):
            self.ashareeodprices('S_DQ_TRADESTATUS')
        return self.ashareeodprices.values.index

class index(meta):
    __tables__ = [aindexeodprices]
    __schemas__ = list(set(['"%s"' %(i.schemas) for i in __tables__]))
    __schemas__ = ('TABLE_SCHEMA = %s' %(__schemas__[0])) if len(__schemas__) == 1 else 'TABLE_SCHEMA IN (%s)' %(','.join(__schemas__))
    __table_name__ = 'TABLE_NAME IN (%s)' %(','.join(['"%s"' %(i.__name__) for i in __tables__]))
    _help = pd.SQL.info(columns = ['TABLE_SCHEMA' ,'TABLE_NAME', 'COLUMN_NAME', 'COLUMN_COMMENT'], where = ' AND '.join([__schemas__, __table_name__]))



