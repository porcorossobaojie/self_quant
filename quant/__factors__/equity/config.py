# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 17:45:49 2022

@author: Porco Rosso
"""


class main():
    params = {'asharebalancesheet': ['INVENTORIES', 'MONETARY_CAP', 'TOT_CUR_ASSETS', 'TOT_CUR_LIAB', 'TOT_ASSETS', 'TOT_LIAB'], 
              'asharecashflow': ['CASH_CASH_EQU_END_PERIOD', 'NET_CASH_FLOWS_OPER_ACT', 'PLUS_PROV_DEPR_ASSETS'],
              'asharefinancialindicator': ['CASH_TTM_TO_MKT', 'DEGM', 'EBIT', 'INTANG_ASSET_RATIO', 'INVENTORY_TURNOVER_RATIO', 'NET_ASSET_TO_MKT', 'NET_LIAB', 
                                           'NET_OPER_CASH_RATIO', 'NET_OPER_CASH_TTM', 'NET_PROFIT_TTM', 'OPER_CASH_TO_OPER_REV', 'OPER_REV_TTM', 'ROA_TTM', 'TOT_PROFIT_TTM', 
                                           'OPER_CASH_GROWTH_RATIO', 'OPER_PROFIT_GROWTH_RATIO', 'OPER_REV_GROWTH_RATIO', 'TOT_ASSET_GROWTH_RATIO'], 
              'ashareincome': ['TOT_PROFIT', 'TOT_OPER_COST', 'TOT_OPER_REV', ],
              'ashareperformanceletter': ['TOT_OPER_REV_LT', 'OPER_PROFIT_LT', 'TOT_ASSETS_LT', 'TOT_PROFIT_LT'],
              'ashareindustriesclass': ['S_JQL1_CODE', 'S_JQL2_CODE'],
              'ashareeodprices': ['S_DQ_CLOSE', 'S_DQ_TRADESTATUS', 'S_DQ_PCTCHANGE'], 
              'ashareeodderivativeindicator': ['S_VAL_MV', 'S_DQ_PB', 'S_DQ_PCF_TTM', 'S_DQ_PE_TTM', 'S_DQ_PS_TTM']}

