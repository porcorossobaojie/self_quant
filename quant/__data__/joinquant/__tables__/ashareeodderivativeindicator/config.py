# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 14:18:40 2021

@author: Porco Rosso
"""
import pandas as pd

class main():
    params = {'table': 'ashareeodderivativeindicator', 
              'source_key': ['day', 'code', 'capitalization', 'circulating_cap', 'market_cap', 'circulating_market_cap', 'turnover_ratio', 'pe_ratio', 'pe_ratio_lyr', 'pb_ratio', 'ps_ratio', 'pcf_ratio', 'pcf_ratio2', 'dividend_ratio'],
              'columns': {'TRADE_DT': ['datetime', '交易日'], 
                          'S_INFO_WINDCODE': ['varchar(12)', '股票代码'], 
                          'S_VAL_SHR': ['double(20, 4)', '总股本'],
                          'S_DQ_SHR': ['double(20, 4)', '流通股本'],
                          'S_VAL_MV': ['double(20, 4)', '总市值'], 
                          'S_DQ_MV': ['double(20, 4)', '流通市值'],
                          'S_DQ_FREETURNOVER': ['double(20, 4)', '换手率\n[指定交易日成交量(手)100/截至该日股票的自由流通股本(股)]*100%'], 
                          'S_DQ_PE_TTM': ['double(20, 4)', '市盈率(PE, TTM)\n市盈率（PE，TTM）=（股票在指定交易日期的收盘价 * 当日人民币外汇挂牌价* 截止当日公司总股本）/归属于母公司股东的净利润TTM'], 
                          'S_DQ_PE_LYR': ['double(20, 4)', '市盈率(PE, LYR)\n市盈率（PE）=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/归属母公司股东的净利润'], 
                          'S_DQ_PB': ['double(20,4)', '市净率(PB)\n市净率=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/归属母公司股东的权益'], 
                          'S_DQ_PS_TTM': ['double(20, 4)', '市销率(PS, TTM)\n市销率TTM=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/营业总收入TTM'],
                          'S_DQ_PCF_TTM': ['double(20, 4)', '市现率(PCF, 现金净流量TTM)\n市现率=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM'], 
                          'S_DQ_POCF_TTM':['double(20, 4)', '市现率(PCF, 经营现金净流量TTM)\n市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/经营活动现金及经营活动现金等价物净增加额TTM'], 
                          'S_DQ_DIVRATIO_TTM': ['double(20, 4)', '市现率(PCF, 现金净流量TTM)\n市现率=（（股票在指定交易日期的收盘价 * 截至当日公司总股本）/经营活动现金及经营活动现金等价物净增加额TTM'], }, 
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2005-01-01', '2030-12-31', freq='Y').to_list()}
              }



