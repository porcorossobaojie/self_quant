# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 10:16:37 2021

@author: Porco Rosso
"""

from __factors__.barra.config import main as barra_config
from __factors__.finance.config import main as finance_config
from __factors__.market.config import main as market_config

__dic__ = {}
for i in [barra_config, finance_config, market_config]:
    for key, value in i.params.items():
        __dic__[key] = [columns.upper() for columns in value] if key not in __dic__.keys() else __dic__[key] + [columns.upper() for columns in value] 
__dic__ = {i:list(set(j)) for i,j in __dic__.items()}

class main():
    filter_rule = {'begin': None, 'be_list_limit': 126, 'drop_st': 1, 'trade_status': True}
    table_infomation = __dic__






