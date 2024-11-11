# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 16:11:58 2019

@author: Porco Rosso
"""

import numpy as np




def _ic(factor, returns, rolling):
    return factor.shift().corrwith(returns, axis=1).rolling(rolling).mean()

def _ir(factor, returns, rolling):
    df = factor.shift().corrwith(returns, axis=1)
    df = df.rolling(rolling).mean() / df.rolling(rolling).std()
    df[df.abs() == np.inf] = np.nan
    return df

























    