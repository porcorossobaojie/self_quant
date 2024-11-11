# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 21:10:48 2019

@author: Porco Rosso

    Il n'ya qu'un héroïsme au monde : c'est de voir le monde 
tel qu'il est et de l'aimer

                                        ————    Roman Roland

"""
import pandas as pd
import numpy as np
if pd.__version__ < '1.0.1':
    pd.NA = np.nan

import warnings
warnings.simplefilter(action='ignore')

import __pandas.__SQL
import __pandas.__build
import __pandas.__tools
import __pandas.__stats
import __pandas.__analysis
import __pandas.__roll

import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
