# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:06:11 2021

@author: Porco Rosso
"""




from __factors__.barra.main import main as barra
from __factors__.base.main import main as meta
from __factors__.finance.finance_to_market import main as finance
from __factors__.market.trading import main as trade 

barra = barra()
finance = finance()
trade = trade()
