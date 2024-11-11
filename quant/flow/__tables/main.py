# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:03:11 2021

@author: Porco Rosso
"""

from flow.__tables.meta import meta
from flow.__tables.config import keys, values

class ashareeodprices(meta, type('', (), dict(zip(keys._params, values.ashareeodprices)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class ashareeodprices1min(meta, type('', (), dict(zip(keys._params, values.ashareeodprices1min)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]

class ashareperformanceletter(meta, type('', (), dict(zip(keys._params, values.ashareperformanceletter)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]

class ashareorder(meta, type('', (), dict(zip(keys._params, values.ashareorder)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class ashareconnect(meta, type('', (), dict(zip(keys._params, values.ashareconnect)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class ashareeodderivativeindicator(meta, type('', (), dict(zip(keys._params, values.ashareeodderivativeindicator)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class asharebalancesheet(meta, type('', (), dict(zip(keys._params, values.asharebalancesheet)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class asharecashflow(meta, type('', (), dict(zip(keys._params, values.asharecashflow)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]

class ashareincome(meta, type('', (), dict(zip(keys._params, values.ashareincome)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class asharefinancialindicator(meta, type('', (), dict(zip(keys._params, values.asharefinancialindicator)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
        
class ashareindustriesclass(meta, type('', (), dict(zip(keys._params, values.ashareindustriesclass)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]

class aindexeodprices(meta, type('', (), dict(zip(keys._params, values.aindexeodprices)))):
    def __init__(self, **kwargs):
        [setattr(self, i, j) for i,j in kwargs.items() if i in keys._params]
                

    


        












