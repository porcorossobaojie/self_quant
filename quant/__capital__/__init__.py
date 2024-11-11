# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 16:17:42 2021

@author: Porco Rosso
"""

import pandas as pd
from __capital__.main.main import DataFrame, Series

pd._DataFrame = DataFrame
pd._Series = Series



