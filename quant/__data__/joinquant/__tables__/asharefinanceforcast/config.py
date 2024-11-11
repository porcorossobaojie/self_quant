# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:09:32 2021

@author: Porco Rosso
"""

class main():
    params = {'table': 'asharefinanceforcast', 
              'source_key': ['id', 'code', 'pub_date', 'end_date', 'type_id', 'profit_min', 'profit_max', 'profit_last', 'profit_ratio_min', 'profit_ratio_max', 'content'],
              'columns': {'ID_KEY': ['int', '来源自增id'],
                          'S_INFO_WINDCODE': ['varchar(12)', '股票代码'], 
                          'ANN_DT': ['datetime', '公告期'], 
                          'REPORT_PERIOD': ['datetime', '报告期'], 
                          'REPORT_TYPE': ['int', '预告类型: \n 05001: 业绩大幅上升, 305002: 业绩预增,	305003: 业绩预盈, 305004: 预计扭亏, 305005: 业绩持平, 305006: 无大幅变动, 	305007: 业绩预亏, 305008: 业绩大幅下降, 305009: 大幅减亏, 305010: 业绩预降, 305011: 预计减亏, 305012: 不确定, 305013: 取消预测'], 
                          'PROFIT_MIN': ['double(18, 2)', '预告净利润下限'], 
                          'PROFIT_MAX': ['double(18, 2)', '预告净利润上限'], 
                          'PROFIT_LAST_ROUND_PERIOD': ['double(18, 2)', '去年同期净利润'], 
                          'PROFIT_MIN_RATIO': ['double(8, 2)', '预告净利润变动幅度下限'], 
                          'PROFIT_MAX_RATIO': ['double(8, 2)', '预告净利润变动幅度上限'], 
                          'CONTENT': ['varchar(1024)', '预告内容']}, 
              'primary': 'UNIQUE_KEY', 
              'keys': ['ANN_DT', 'REPORT_PERIOD']}



















