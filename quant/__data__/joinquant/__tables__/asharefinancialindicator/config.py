# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 16:03:48 2021

@author: Porco Rosso
"""

import pandas as pd

class main():
    params = {'table': 'asharefinancialindicator', 
              'columns': {'TRADE_DT': ['datetime', '交易日期'], 
                          'S_INFO_WINDCODE': ['varchar(12)', '股票代码'],
                          'net_oper_cap': ['double(20, 4)', '净运营资本	流动资产 － 流动负债'], 
                          'tot_oper_rev_ttm': ['double(20, 4)', '营业总收入TTM	计算过去12个月的 营业总收入 之和'], 
                          'oper_profit_ttm': ['double(20, 4)', '营业利润TTM	计算过去12个月 营业利润 之和'], 
                          'net_oper_cash_ttm': ['double(20, 4)', '经营活动现金流量净额TTM	计算过去12个月 经营活动产生的现金流量净值 之和'], 
                          'oper_rev_ttm': ['double(20, 4)', '营业收入TTM	计算过去12个月的 营业收入 之和'], 
                          'interest_cur_liab': ['double(20, 4)', '带息流动负债	流动负债合计 - 无息流动负债'], 
                          'sale_exp_ttm': ['double(20, 4)', '销售费用TTM	计算过去12个月 销售费用 之和'], 
                          'retain_earn': ['double(20, 4)', '留存收益	盈余公积金+未分配利润'], 
                          'tot_oper_cost_ttm': ['double(20, 4)', '营业总成本TTM	计算过去12个月的 营业总成本 之和'], 
                          'non_oper_net_profit_ttm': ['double(20, 4)', '营业外收支净额TTM	营业外收入（TTM） - 营业外支出（TTM）'], 
                          'net_inv_cash_ttm': ['double(20, 4)', '投资活动现金流量净额TTM	计算过去12个月 投资活动现金流量净额 之和'], 
                          'fin_exp_ttm': ['double(20, 4)', '财务费用TTM	计算过去12个月 财务费用 之和'], 
                          'admin_exp_ttm': ['double(20, 4)', '管理费用TTM	计算过去12个月 管理费用 之和'], 
                          'net_interest_exp': ['double(20, 4)', '净利息费用	利息支出-利息收入'], 
                          'val_chg_profit_ttm': ['double(20, 4)', '价值变动净收益TTM	计算过去12个月 价值变动净收益 之和'], 
                          'tot_profit_ttm': ['double(20, 4)', '利润总额TTM	计算过去12个月 利润总额 之和'], 
                          'net_fin_cash_flow_ttm': ['double(20, 4)', '筹资活动现金流量净额TTM	计算过去12个月 筹资活动现金流量净额 之和'], 
                          'interest_free_cur_liab': ['double(20, 4)', '无息流动负债	应付票据+应付账款+预收账款(用 预收款项 代替)+应交税费+应付利息+其他应付款+其他流动负债'], 
                          'ebit': ['double(20, 4)', '息税前利润	净利润+所得税+财务费用'], 
                          'net_profit_ttm': ['double(20, 4)', '净利润TTM	计算过去12个月 净利润 之和'], 
                          'oper_net_inc': ['double(20, 4)', '经营活动净收益	经营活动净收益/利润总额'], 
                          'asset_loss_ttm': ['double(20, 4)', '资产减值损失TTM	计算过去12个月 资产减值损失 之和'], 
                          'par_comp_net_inc_ttm': ['double(20, 4)', '归属于母公司股东的净利润TTM	计算过去12个月 归属于母公司股东的净利润 之和'], 
                          'oper_cost_ttm': ['double(20, 4)', '营业成本TTM	计算过去12个月的 营业成本 之和'], 
                          'net_liab': ['double(20, 4)', '净债务	总债务-期末现金及现金等价物余额'], 
                          'net_profit_to_tot_oper_rev_ttm': ['double(20, 4)', '净利润与营业总收入之比	净利润与营业总收入之比=净利润（TTM）/营业总收入（TTM）'], 
                          'net_profit_ratio': ['double(20, 4)', '销售净利率	售净利率=净利润（TTM）/营业收入（TTM）'], 
                          'net_non_oper_inc_to_tot_profit': ['double(20, 4)', '营业外收支利润净额/利润总额	营业外收支利润净额/利润总额'], 
                          'degm': ['double(20, 4)', '毛利率增长   今年毛利（TTM） / 今年总营收（TTM） - 去年毛利（TTM） / 去年总营收（TTM）'], 
                          'sale_exp_to_oper_rev': ['double(20, 4)', '营业费用与营业总收入之比	营业费用与营业总收入之比=销售费用（TTM）/营业总收入（TTM）'], 
                          'net_oper_cash_ratio': ['double(20, 4)', '净利润现金含量	经营活动产生的现金流量净额/归属于母公司所有者的净利润'], 
                          'intang_asset_ratio': ['double(20, 4)', '无形资产比率	无形资产比率=(无形资产+研发支出+商誉)/总资产'], 
                          'inventory_turnover_ratio': ['double(20, 4)', '存货周转率	存货周转率=营业成本（TTM）/存货'], 
                          'oper_profit_growth_ratio': ['double(20, 4)', '营业利润增长率   今年营业利润（TTM） / 今年营业收入（TTM） -  去年营业利润（TTM） / 去年营业收入（TTM）'], 
                          'net_oper_cash_to_net_debt': ['double(20, 4)', '经营活动产生现金流量净额/净债务	经营活动产生现金流量净额/净债务'], 
                          'net_oper_cash_to_tot_asset': ['double(20, 4)', '总资产现金回收率	经营活动产生的现金流量净额(ttm) / 总资产 '], 
                          'oper_profit_to_tot_profit': ['double(20, 4)', '经营活动净收益/利润总额	经营活动净收益/利润总额'], 
                          'oper_cash_to_oper_rev': ['double(20, 4)', '经营活动产生的现金流量净额与营业收入之比	经营活动产生的现金流量净额（TTM） / 营业收入（TTM）'], 
                          'roa_ttm': ['double(20, 4)', '资产回报率TTM	资产回报率=净利润（TTM）/期初总资产'], 
                          'roe_ttm': ['double(20, 4)', '权益回报率TTM	权益回报率=净利润（TTM）/期初股东权益'], 
                          'oper_rev_growth_ratio': ['double(20, 4)', '营业收入增长率	营业收入增长率=（今年营业收入（TTM）/去年营业收入（TTM））-1'], 
                          'tot_asset_growth_ratio': ['double(20, 4)', '总资产增长率	总资产 / 总资产_4 -1'], 
                          'oper_cash_growth_ratio': ['double(20, 4)', '经营活动产生的现金流量净额增长率	(今年经营活动产生的现金流量净额（TTM）/去年经营活动产生的现金流量净额（TTM）)-1'], 
                          'tot_oper_rev_ttm_to_mkt': ['double(20, 10)', '股营业总收入TTM	营业总收入（TTM）除以总市值'], 
                          'cash_equity_to_mkt': ['double(20, 10)', '每股现金及现金等价物余额	每市值现金及现金等价物余额'], 
                          'oper_rev_ttm_to_mkt': ['double(20, 10)', '每股营业收入TTM	营业收入（TTM）除以总市值'], 
                          'net_asset_to_mkt': ['double(20, 10)', '每股净资产	归属母公司所有者权益合计除以总市值'], 
                          'oper_cash_ttm_to_mkt': ['double(20, 10)', '每市值经营活动产生的现金流量净额	每股经营活动产生的现金流量净额'], 
                          'oper_profit_ttm_to_mkt': ['double(20, 10)', '每股营业利润TTM	营业利润（TTM）除以总市值'], 
                          'eps_ttm': ['double(20, 10)', '过去12个月归属母公司所有者的净利润（TTM）除以总股本市值'], 
                          'cash_ttm_to_mkt': ['double(20, 10)', '每股现金流量净额，根据当时日期来获取最近变更日的总股本	现金流量净额（TTM）除以总市值']},
              'primary': 'UNIQUE_KEY', 
              'keys': ['TRADE_DT', 'S_INFO_WINDCODE'], 
              'partition': {'TRADE_DT': pd.date_range('2005-01-01', '2030-12-31', freq='Y').to_list()}}












