# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 16:37:01 2022

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
        me = self.stock('S_VAL_MV')
        





