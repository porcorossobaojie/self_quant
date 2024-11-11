# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:39:09 2021

@author: Porco Rosso
"""

from __data__.joinquant.__tables__.aindexeodprices.main import main as aindexeodprices
from __data__.joinquant.__tables__.asharebalancesheet.main import main as asharebalancesheet
from __data__.joinquant.__tables__.asharecashflow.main import main as asharecashflow
from __data__.joinquant.__tables__.asharedescription.main import main as asharedescription
from __data__.joinquant.__tables__.asharedividend.main import main as asharedividend
from __data__.joinquant.__tables__.ashareeodderivativeindicator.main import main as ashareeodderivativeindicator
from __data__.joinquant.__tables__.ashareeodprices.main import main as ashareeodprices
from __data__.joinquant.__tables__.ashareeodprices1min.main import main as ashareeodprices1min
from __data__.joinquant.__tables__.asharefinanceforcast.main import main as asharefinanceforcast
from __data__.joinquant.__tables__.ashareincome.main import main as ashareincome
from __data__.joinquant.__tables__.ashareindustriesclass.main import main as ashareindustriesclass
from __data__.joinquant.__tables__.asharestatus.main import main as asharestatus
from __data__.joinquant.__tables__.aindexhs300freeweight.main import main as aindexhs300freeweight
from __data__.joinquant.__tables__.ashareconnect.main import main as ashareconnect
from __data__.joinquant.__tables__.ashareorder.main import main as ashareorder
from __data__.joinquant.__tables__.ashareperformanceletter.main import main as ashareperformanceletter

def daily(replace=False):
    if replace:
        check = input('Please check and make sure rebuilding ')
    for i in [aindexeodprices,  aindexhs300freeweight, #指数 成分股权重
              asharebalancesheet, asharecashflow, ashareincome, #三大财报
              ashareperformanceletter, asharefinanceforcast, #业绩快报 业绩预告
              asharedescription,  #上退市日期
              asharedividend, ashareconnect,ashareorder, #分红 沪港通 主力大小单
              ashareindustriesclass, # 行业分类
              ashareeodderivativeindicator, #市值换手率等
              asharestatus, #ST
              ashareeodprices, #ashareeodprices1min, #日交易数据
              ]: 
        instance = i()
        if replace:
            instance.daily('replace')
        else:
            instance.daily()
    from __data__.joinquant.__tables__.asharefinancialindicator.main import main as asharefinancialindicator
    instance = asharefinancialindicator()
    if replace:
        instance.daily('replace')
    else:
        instance.daily()
        















