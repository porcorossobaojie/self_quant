# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 09:59:44 2021

@author: Porco Rosso
"""

class main():
    params = {'table': 'asharedividend', 
              'source_key': ['id', 'company_name', 'code', 'report_date', 
                             'board_plan_pub_date', 'board_plan_bonusnote', 
                             'shareholders_plan_pub_date', 'shareholders_plan_bonusnote',
                             'implementation_pub_date', 'implementation_bonusnote',
                             'dividend_ratio', 'transfer_ratio', 'bonus_ratio_rmb', 
                             'a_registration_date', 'a_xr_date', 'a_bonus_date', 
                             'plan_progress_code', 'bonus_cancel_pub_date'],
              'columns': {'ID_KEY': ['int', '来源自增id'],
                          'S_INFO_COMPANYNAME': ['varchar(128)', '公司全称'],
                          'S_INFO_WINDCODE': ['VARCHAR(16)', '股票代码'], 
                          'REPORT_PERIOD': ['datetime', '分红报告期'],
                          
                          'BOARD_PLAN_DT': ['datetime', '董事会预案公告日期'], 
                          'BOARD_PLAN_NOTE': ['varchar(128)', '董事会预案分红说明'], 
                          
                          'SHAREHOLDER_PLAN_DT': ['datetime', '股东大会预案公告日期'], 
                          'SHAREHOLDER_PLAN_NOTE':  ['varchar(128)', '股东大会预案分红说明'],
                          
                          'IMPLEMENT_DT': ['datetime', '实施方案公告日期'], 
                          'IMPLEMENT_NOTE': ['varchar(128)', '实施方案分红说明'], 
                          
                          'S_DIV_BONUSRATE': ['double(8, 4)', '送股比例'], 
                          'S_DIV_CONVERSEDRATE': ['double(8, 4)', '转增比例'], 
                          'S_DIV_CASH': ['double(12, 4)', '派息比例(人民币)'], 
                          
                          'REGISTRATION_DT': ['datetime', '股权登记日'], 
                          'EX_DT': ['datetime', '除权日'], 
                          'DVD_PAYOUT_DT': ['datetime', '派息日'], 
                          'S_DIV_PROGRESS': ['int', '313001-董事会预案, 313002-实施方案, 313003-股东大会预案, 313004-取消分红, 313005-公司预案'], 
                          'CANCEL_DT': ['datetime', '取消分红公告日期'], 
                          'S_DIV_TOTAL': ['double(8, 4)', '送转增总和']},
              'primary': 'UNIQUE_KEY',
              'keys': ['ID_KEY', 'EX_DT', 'DVD_PAYOUT_DT'],
              'partition': {'S_DIV_PROGRESS': [313001, 313002, 313003, 313004, 313005]}
                }




