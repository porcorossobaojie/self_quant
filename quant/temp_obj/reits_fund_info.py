# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 08:56:24 2023

@author: Porco Rosso
"""

import __data__
import jqdatasdk as jq
import pandas as pd

df = jq.get_all_securities(['fund'])
df = df[df.type.str.contains("reits") ]

base_info = [jq.finance.run_query(jq.query(jq.finance.FUND_MAIN_INFO).filter(jq.finance.FUND_MAIN_INFO.main_code==i[:6])) for i in df.index]
base_info = pd.concat(base_info)
'''

字段	名称	类型
main_code	基金主体代码	varchar(12)
name	基金名称	varchar(100)
advisor	基金管理人	varchar(100)
trustee	基金托管人	varchar(100)
operate_mode_id	基金运作方式编码	int
operate_mode	基金运作方式	varchar(32)
underlying_asset_type_id	投资标的类型编码	int
underlying_asset_type	投资标的类型	varchar(32)
start_date	成立日期	date
pub_date	发行日期	date
end_date	结束日期	date
invest_style_id	投资风格编码	int
invest_style	投资风格	varchar(32)
statistics_main_code	基金统计主代码（仅多份额基金存在此字段
'''

portfolio_info = [jq.finance.run_query(jq.query(jq.finance.FUND_PORTFOLIO).filter(jq.finance.FUND_PORTFOLIO.code==i[:6])) for i in df.index]
portfolio_info = pd.concat(portfolio_info)

'''
code	基金代码	varchar(12)
name	基金名称	varchar(80)
period_start	开始日期	date
period_end	报告期	date
pub_date	公告日期	date
report_type_id	报告类型编码	int
report_type	报告类型	varchar(32)
equity_value	权益类投资金额	decimal(20,4)
equity_rate	权益类投资占比	decimal(10,4)
stock_value	股票投资金额	decimal(20,4)
stock_rate	股票投资占比	decimal(10,4)
fixed_income_value	固定收益投资金额	decimal(20,4)
fixed_income_rate	固定收益投资占比	decimal(10,4)
precious_metal_value	贵金属投资金额	decimal(20,4)
precious_metal_rate	贵金属投资占比	decimal(10,4)
derivative_value	金融衍生品投资金额	decimal(20,4)
derivative_rate	金融衍生品投资占比	decimal(10,4)
buying_back_value	买入返售金融资产金额	decimal(20,4)
buying_back_rate	买入返售金融资产占比	decimal(10,4)
deposit_value	银行存款和结算备付金合计	decimal(20,4)
deposit_rate	银行存款和结算备付金合计占比	decimal(10,4)
others_value	其他资产	decimal(20,4)
others_rate	其他资产占比	decimal(10,4)
total_asset	总资产合计	decimal(20,4)
'''
finance_info =  [jq.finance.run_query(jq.query(jq.finance.FUND_FIN_INDICATOR).filter(jq.finance.FUND_FIN_INDICATOR.code==i[:6])) for i in df.index]
finance_info = pd.concat(finance_info)

'''
code	基金代码	varchar(12)
name	基金名称	varchar(80)
period_start	开始日期	date
period_end	结束日期	date
pub_date	公告日期	date
report_type_id	报告类型编码	int
report_type	报告类型	varchar(32)
profit	本期利润	
adjust_profit	本期利润扣减本期公允价值变动损益后的净额	
avg_profit	加权平均份额本期利润	
avg_roe	加权平均净值利润率	
profit_available	期末可供分配利润	
profit_avaialbe_per_share	期末可供分配份额利润	
total_tna	期末基金资产净值	
nav	期末基金份额净值	
adjust_nav	期末还原后基金份额累计净值	
nav_growth	本期净值增长率	
acc_nav_growth	累计净值增长率	
adjust_nav_growth	扣除配售新股基金净值增长率
'''

divid_info = [jq.finance.run_query(jq.query(jq.finance.FUND_DIVIDEND).filter(jq.finance.FUND_DIVIDEND.code==i[:6])) for i in df.index]
divid_info = pd.concat(divid_info)
'''
code	基金代码	varchar(12)
name	基金名称	varchar(80)
pub_date	公布日期	date
event_id	事项类别	int
event	事项名称	varchar(100)
distribution_date	分配收益日	date
process_id	方案进度编码	int
process	方案进度	varchar(100)
proportion	派现比例	decimal(20,8)
split_ratio	分拆（合并、赠送）比例	decimal(20,8)
record_date	权益登记日	date
ex_date	除息日	date
fund_paid_date	基金红利派发日	date
redeem_date	再投资赎回起始日	date
dividend_implement_date	分红实施公告日	dated
dividend_cancel_date	取消分红公告日	date
otc_ex_date	场外除息日	date
pay_date	红利派发日	date
new_share_code	新增份额基金代码	varchar(10)
new_share_name	新增份额基金名称	varchar(100)
'''


net_info =  [jq.finance.run_query(jq.query(jq.finance.FUND_NET_VALUE).filter(jq.finance.FUND_NET_VALUE.code==i[:6])) for i in df.index]
net_info = pd.concat(net_info)
'''
code	基金代码	varchar(12)	
day	交易日	date	
net_value	单位净值	decimal(20,6)	基金单位净值=（基金资产总值－基金负债）÷ 基金总份额
sum_value	累计净值	decimal(20,6)	累计单位净值＝单位净值＋成立以来每份累计分红派息的金额
factor	复权因子	decimal(20,6)	交易日最近一次分红拆分送股的复权因子
acc_factor	累计复权因子	decimal(20,6)	基金从上市至今累计分红拆分送股的复权因子
refactor_net_value	累计复权净值	decimal(20,6)	复权单位净值＝单计净值＋成立以来每份累计分红派息的金额（1+涨跌幅）
'''










