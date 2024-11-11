# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:27:16 2021

@author: Porco Rosso
"""

import pandas as pd

SCHEMAS = 'join_data'

class keys():
    _params = ['schemas', 'table', 'filter_key', 'filter_max', 'filter_min', 'index', 'columns', 'where', 'values']
    
class values():
    ashareperformanceletter = [SCHEMAS, 'ashareperformanceletter', 
                            'ANN_DT', None, None, 
                            'REPORT_PERIOD', 'S_INFO_WINDCODE', 
                            None, pd.DataFrame()]    
    
    ashareorder = [SCHEMAS, 'ashareorder', 
                        None, None, None, 
                        'TRADE_DT', 'S_INFO_WINDCODE', 
                        None, pd.DataFrame()]
    
    ashareconnect = [SCHEMAS, 'ashareconnect', 
                        None, None, None, 
                        'TRADE_DT', 'S_INFO_WINDCODE', 
                        None, pd.DataFrame()]
    
    ashareeodprices = [SCHEMAS, 'ashareeodprices', 
                        None, None, None, 
                        'TRADE_DT', 'S_INFO_WINDCODE', 
                        None, pd.DataFrame()]
    
    ashareeodprices1min = [SCHEMAS, 'ashareeodprices1min', 
                        None, None, None, 
                        'TRADE_DT', 'S_INFO_WINDCODE', 
                        None, pd.DataFrame()]

    ashareeodderivativeindicator = [SCHEMAS, 'ashareeodderivativeindicator', 
                                    None, None, None, 
                                    'TRADE_DT', 'S_INFO_WINDCODE', 
                                    None, pd.DataFrame()]
    
    asharebalancesheet = [SCHEMAS, 'asharebalancesheet', 
                            'ANN_DT', None, None, 
                            'REPORT_PERIOD', 'S_INFO_WINDCODE', 
                            None, pd.DataFrame()]
    
    asharecashflow = [SCHEMAS, 'asharecashflow', 
                        'ANN_DT', None, None, 
                        'REPORT_PERIOD', 'S_INFO_WINDCODE', 
                        None, pd.DataFrame()]
    
    ashareincome = [SCHEMAS, 'ashareincome', 
                    'ANN_DT', None, None, 
                    'REPORT_PERIOD', 'S_INFO_WINDCODE', 
                    None, pd.DataFrame()]
    
    asharefinancialindicator = [SCHEMAS, 'asharefinancialindicator', 
                                None, None, None, 
                                'TRADE_DT', 'S_INFO_WINDCODE', 
                                None, pd.DataFrame()]
    
    ashareindustriesclass = [SCHEMAS, 'ashareindustriesclass', 
                             None, None, None, 
                             'TRADE_DT', 'S_INFO_WINDCODE', 
                             None, pd.DataFrame()]
    
    aindexeodprices = [SCHEMAS, 'aindexeodprices', 
                        None, None, None, 
                        'TRADE_DT', 'S_INFO_WINDCODE', 
                        "S_INFO_WINDCODE IN ('000852.SH', '000905.SH', '399300.SZ', '000016.SH', '000852.XSHG', '000905.XSHG', '399300.XSHE', '000016.XSHE')", pd.DataFrame()]  
    
    aindexhs300freeweight = [SCHEMAS, 'aindexhs300freeweight', 
                             'ANN_DT', None, None, 
                             'REPORT_PERIOD', 'S_INFO_WINDCODE', 
                             None, pd.DataFrame()]


