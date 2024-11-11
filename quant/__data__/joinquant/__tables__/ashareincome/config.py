# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 09:32:54 2021

@author: Porco Rosso
"""

from numpy import nan
import pandas as pd

df = {
     0: {'source_key': 'company_name', 'save_key': nan, 'data_type': 'varchar(100)', 'comment': '公司名称\n'},
     1: {'source_key': 'code', 'save_key': 's_info_windcode', 'data_type': 'varchar(12)', 'comment': '股票代码\n'},
     2: {'source_key': 'a_code', 'save_key': nan, 'data_type': 'varchar(12)', 'comment': 'A股代码\n'},
     3: {'source_key': 'b_code', 'save_key': nan, 'data_type': 'varchar(12)', 'comment': 'B股代码\n'},
     4: {'source_key': 'h_code', 'save_key': nan, 'data_type': 'varchar(12)', 'comment': 'H股代码\n'},
     5: {'source_key': 'pub_date', 'save_key': 'ann_dt', 'data_type': 'datetime', 'comment': '公告日期\n'},
     6: {'source_key': 'start_date', 'save_key': nan, 'data_type': 'datetime', 'comment': '开始日期\n'},
     7: {'source_key': 'end_date', 'save_key': nan, 'data_type': 'datetime', 'comment': '截止日期\n'},
     8: {'source_key': 'report_date', 'save_key': 'report_period', 'data_type': 'datetime', 'comment': '报告期\n'},
     9: {'source_key': 'id', 'save_key': 'id_key', 'data_type': 'int', 'comment': '来源自增ID\n'},
     10: {'source_key': 'source_id', 'save_key': nan, 'data_type': 'int', 'comment': '报表来源编码\n'},
     11: {'source_key': 'source', 'save_key': nan, 'data_type': 'varchar(60)', 'comment': '报表来源\n'},
     12: {'source_key': 'total_operating_revenue', 'save_key': 'tot_oper_rev', 'data_type': 'decimal(20,4)', 'comment': '营业总收入\n具体核算范围和方法参见上市公司定期报告'},
     13: {'source_key': 'operating_revenue', 'save_key': 'oper_rev', 'data_type': 'decimal(20,4)', 'comment': '营业收入\n具体核算范围和方法参见上市公司定期报告'},
     14: {'source_key': 'total_operating_cost', 'save_key': 'tot_oper_cost', 'data_type': 'decimal(20,4)', 'comment': '营业总成本\n营业总成本=主营业务成本+其他业务成本+利息支出+手续费及佣金支出+退保金+赔付支出净额+提取保险合同准备金净额+保单红利支出+分保费用+营业税金及附加+销售费用+管理费用+财务费用+资产减值损失+其他'},
     15: {'source_key': 'operating_cost', 'save_key': 'oper_cost', 'data_type': 'decimal(20,4)', 'comment': '营业成本\n营业成本，也称运营成本。是指企业所销售商品或者提供劳务的成本。营业成本应当与所销售商品或者所提供劳务而取得的收入进行配比。'},
     16: {'source_key': 'operating_tax_surcharges', 'save_key': 'less_taxes_surcharges_ops', 'data_type': 'decimal(20,4)', 'comment': '营业税金及附加\n反映企业经营主要业务应负担的营业税、消费税、城市维护建设税、资源税和教育费附加等。填报此项指标时应注意，实行新税制后，会计上规定应交增值税不再计入“主营业务税金及附加”项，无论是一般纳税企业还是小规模纳税企业均应在“应交增值税明细表”中单独反映。根据企业会计“利润表”中对应指标的本年累计数填列。'},
     17: {'source_key': 'sale_expense', 'save_key': 'less_selling_dist_exp', 'data_type': 'decimal(20,4)', 'comment': '销售费用\n销售费用是指企业在销售产品、自制半成品和提供劳务等过程中发生的各项费用。包括由企业负担的包装费、运输费、广告费、装卸费、保险费、委托代销手续费、展览费、租赁费（不含融资租赁费)和销售服务费、销售部门人员工资、职工福利费、差旅费、折旧费、修理费、物料消耗、低值易耗品摊销以及其他经费等。与销售有关的差旅费应计入销售费用。'},
     18: {'source_key': 'administration_expense', 'save_key': 'less_gerl_admin_exp', 'data_type': 'decimal(20,4)', 'comment': '管理费用\n管理费用是指 企业行政管理部门为组织和管理生产经营活动而发生的各项费用。管理费用属于期间费用，在发生的当期就计入当期的损失或是利益。'},
     19: {'source_key': 'exploration_expense', 'save_key': 'less_expl_exp', 'data_type': 'decimal(20,4)', 'comment': '堪探费用\n'},
     20: {'source_key': 'financial_expense', 'save_key': 'less_fin_exp', 'data_type': 'decimal(20,4)', 'comment': '财务费用\n财务费用指企业在生产经营过程中为筹集资金而发生的筹资费用。包括企业生产经营期间发生的利息支出（减利息收入）、汇兑损益（有的企业如商品流通企业、保险企业进行单独核算，不包括在财务费用）、金融机构手续费，企业发生的现金折扣或收到的现金折扣等。但在企业筹建期间发生的利息支出，应计入开办费；为购建或生产满足资本化条件的资产发生的应予以资本化的借款费用，在“在建工程”、“制造费用”等账户核算。'},
     21: {'source_key': 'asset_impairment_loss', 'save_key': 'less_impair_loss_assets', 'data_type': 'decimal(20,4)', 'comment': '资产减值损失\n资产减值损失是指因资产的账面价值高于其可收回金额而造成的损失。 新会计准则规定资产减值范围主要是固定资产、无形资产以及除特别规定外的其他资产减值的处理。《资产减值》准则改变了固定资产、无形资产等的减值准备计提后可以转回的做法，资产减值损失一经确认，在以后会期间不得转回，消除了一些企业通过计提秘密准备来调节利润的可能，限制了利润的人为波动。资产减值损失在会计核算中属于损益类科目。'},
     22: {'source_key': 'fair_value_variable_income', 'save_key': 'plus_net_gain_chg_fv', 'data_type': 'decimal(20,4)', 'comment': '公允价值变动净收益\n“公允价值变动收益” 这个科目，是“以公允价值计量且其变动计入当期损益的交易性金融资产”的一个科目。在资产负债表日，“交易性金融资产”的公允价值高于其账面价值的差额，应借记“交易性金融资产－公允价值变动”，贷记“公允价值变动损益”，公允价值低于其账面价值的差额，则做相反的分录。'},
     23: {'source_key': 'investment_income', 'save_key': 'plus_net_invest_inc', 'data_type': 'decimal(20,4)', 'comment': '投资收益\n投资收益是对外投资所取得的利润、股利和债券利息等收入减去投资损失后的净收益。严格地讲，所谓投资收益是指以项目为边界的货币收入等。'},
     24: {'source_key': 'invest_income_associates', 'save_key': 'incl_inc_invest_assoc_jv_entp', 'data_type': 'decimal(20,4)', 'comment': '对联营企业和合营企业的投资收益\n持有的对联营企业及合营企业的投资，按照《企业会计准则第2号——长期股权投资》的规定，应当采用权益法核算，在按持股比例等计算确认应享有或应分担被投资单位的净损益时，应当考虑以下因素：投资企业与联营企业及合营企业之间发生的内部交易损益按照持股比例计算归属于投资企业的部分，应当予以抵销，在此基础上确认投资损益。<br>投资企业与被投资单位发生的内部交易损失，按照《企业会计准则第8号———资产减值》等规定属于资产减值损失的，应当全额确认。<br>投资企业对于纳入其合并范围的子公司与其联营企业及合营企业之间发生的内部交易损益，也应当按照上述原则进行抵销，在此基础上确认投资损益。<br>投资企业对于首次执行日之前已经持有的对联营企业及合营企业的长期股权投资，如存在与该投资相关的股权投资借方差额，还应扣除按原剩余期限直线摊销的股权投资借方差额，确认投资损益。<br>投资企业在被投资单位宣告发放现金股利或利润时，按照规定计算应分得的部分确认应收股利，同时冲减长期股权投资的账面价值。'},
     25: {'source_key': 'exchange_income', 'save_key': 'plus_net_gain_fx_trans', 'data_type': 'decimal(20,4)', 'comment': '汇兑收益\n汇兑收益，是指用记账本位币，按照不同的汇率报告相同数量的外币而产生的差额。简单地说，就是公司的外币货币性项目和非货币性项目因汇率变动，在折算成本币时造成损益。而这部分汇兑差额作为财务费用，计入当期损益，从而影响公司利润。'},
     26: {'source_key': 'other_items_influenced_income', 'save_key': 'net_inc_other_ops', 'data_type': 'decimal(20,4)', 'comment': '影响营业利润的其他科目\n'},
     27: {'source_key': 'operating_profit', 'save_key': 'oper_profit', 'data_type': 'decimal(20,4)', 'comment': '营业利润\n营业利润是企业最基本经营活动的成果，也是企业一定时期获得利润中最主要、最稳定的来源。2006年财政部颁布的新企业会计准则-30号财务报表列报中已对营业利润进行了调整，将投资收益调入营业利润，同时取消了主营业务利润和其他业务利润的提法，补贴收入被并入营业外收入，营业利润减营业外收支调整即得到利润总额。'},
     28: {'source_key': 'subsidy_income', 'save_key': 'subsidy_inc', 'data_type': 'decimal(20,4)', 'comment': '补贴收入\n'},
     29: {'source_key': 'non_operating_revenue', 'save_key': 'plus_non_oper_rev', 'data_type': 'decimal(20,4)', 'comment': '营业外收入\n营业外收入是指企业确认与企业生产经营活动没有直接关系的各种收入。'},
     30: {'source_key': 'non_operating_expense', 'save_key': 'less_non_oper_exp', 'data_type': 'decimal(20,4)', 'comment': '营业外支出\n营业外支出是企业发生的与其日常活动无直接关系的各项损失，主要包括非流动资产处置损失、公益性捐赠支出、盘亏损失、非常损失、罚款支出等。'},
     31: {'source_key': 'disposal_loss_non_current_liability', 'save_key': 'less_net_loss_disp_noncur_asset', 'data_type': 'decimal(20,4)', 'comment': '非流动资产处置净损失\n“非流动资产处置损失”属于损益类的科目，在编制利润表时这些科目如果有本期发生额，要填在利润表中。“非流动资产处置损失”是营业外支出的明细科目，在损益表中计入“营业外支出”，“营业外支出”下方会单独列示“非流动资产处置损失”，但是包括在“营业外支出”项目中。'},
     32: {'source_key': 'other_items_influenced_profit', 'save_key': 'oth_infc_profit', 'data_type': 'decimal(20,4)', 'comment': '影响利润总额的其他科目\n'},
     33: {'source_key': 'total_profit', 'save_key': 'tot_profit', 'data_type': 'decimal(20,4)', 'comment': '利润总额\n利润总额指企业在生产经营过程中各种收入扣除各种耗费后的盈余，反映企业在报告期内实现的盈亏总额。'},
     34: {'source_key': 'income_tax', 'save_key': 'inc_tax', 'data_type': 'decimal(20,4)', 'comment': '所得税\n所得税费用是指企业经营利润应交纳的所得税。“所得税费用”，核算企业负担的所得税，是损益类科目；这一般不等于当期应交所得税，因为可能存在“暂时性差异”。如果只有永久性差异，则等于当期应交所得税。'},
     35: {'source_key': 'other_items_influenced_net_profit', 'save_key': 'oth_infc_net_profit', 'data_type': 'decimal(20,4)', 'comment': '影响净利润的其他科目\n'},
     36: {'source_key': 'net_profit', 'save_key': 'net_profit', 'data_type': 'decimal(20,4)', 'comment': '净利润\n净利润（收益）是指在利润总额中按规定交纳了所得税后公司的利润留成，一般也称为税后利润或净利润。净利润的计算公式为：净利润=利润总额-所得税费用.净利润是一个企业经营的最终成果，净利润多，企业的经营效益就好；净利润少，企业的经营效益就差，它是衡量一个企业经营效益的主要指标。'},
     37: {'source_key': 'np_parent_company_owners', 'save_key': 'net_profit_parent_comp', 'data_type': 'decimal(20,4)', 'comment': '归属于母公司所有者的净利润\n准确来讲应称之为“归属于上市公司股东的净利润”，这是因为净利润都归属于股东，只是在合并报表中的净利润有一部分是归属于子公司的其它股东的，这些子公司的其它股东也依法按比例享有子公司的净利润。'},
     38: {'source_key': 'minority_profit', 'save_key': 'minority_int_inc', 'data_type': 'decimal(20,4)', 'comment': '少数股东损益\n少数股东损益是一个流量概念，是指公司合并报表的子公司其它非控股股东享有的损益，需要在利润表中予以扣除。利润表的“净利润”项下可以分“归属于母公司所有者的净利润”和“少数股东损益”。其对应的存量概念是“少数股东权益”。'},
     39: {'source_key': 'eps', 'save_key': 'eps', 'data_type': 'decimal(20,4)', 'comment': '每股收益\n'},
     40: {'source_key': 'basic_eps', 'save_key': 's_fa_eps_basic', 'data_type': 'decimal(20,4)', 'comment': '基本每股收益\n理论算法：归属于普通股股东的当期净利润/(当期实际发行在外的普通股加权平均数=∑(发行在外普通股股数×发行在外月份数)／12)'},
     41: {'source_key': 'diluted_eps', 'save_key': 's_fa_eps_diluted', 'data_type': 'decimal(20,4)', 'comment': '稀释每股收益\n理论算法：归属于普通股股东的当期净利润(扣除当期已确认为费用的稀释性潜在普通股的利息、稀释性潜在普通股转换时将产生的收益或费用、相关所得税的影响)/假设稀释性潜在普通股于当期期初(或发行日)已经全部转换为普通股，于此计算的普通股股数的加权平均数。'},
     42: {'source_key': 'other_composite_income', 'save_key': 'other_compreh_inc', 'data_type': 'decimal(20,4)', 'comment': '其他综合收益\n其他综合收益是指企业根据企业会计准则规定未在损益中确认的各项利得和损失扣除所得税影响后的净额。企业在计算利润表中的其他综合收益时，应当扣除所得税影响；在计算合并利润表中的其他综合收益时，除了扣除所得税影响以外，还需要分别计算归属于母公司所有者的其他综合收益和归属于少数股东的其他综合收益。'},
     43: {'source_key': 'total_composite_income', 'save_key': 'tot_compreh_inc', 'data_type': 'decimal(20,4)', 'comment': '综合收益总额\n综合收益总额项目，反映企业净利润与其他综合收益的合计金额。综合收益，包括其他综合收益和综合收益总额。其中，其他综合收益反映企业根据企业会计准则规定未在损益中确认的各项利得和损失扣除所得税影响后的净额；综合收益总额是企业净利润与其他综合收益的合计金额。'},
     44: {'source_key': 'ci_parent_company_owners', 'save_key': 'tot_compreh_inc_parent_comp', 'data_type': 'decimal(20,4)', 'comment': '归属于母公司所有者的综合收益总额\n综合收益是指除所有者的出资额和各种为第三方或客户代收的款项以外的各种收入。根据美国财务会计准则委员会（FASB）1980年在第3号财务会计概念公告(SFAC3）（企业财务报表的要素）（后为1985年发布的SFAC6所取代）的解释，综合收益是指“一个主体在某一期间与非业主方面进行交易或发生其他事项和情况所引起的权益（净资产）变动。它包括这一期间内除业主投资和派给业主款外，一切权益上的变动。”'},
     45: {'source_key': 'ci_minority_owners', 'save_key': 'tot_compreh_inc_min_shrhldr', 'data_type': 'decimal(20,4)', 'comment': '归属于少数股东的综合收益总额\n综合收益是指除所有者的出资额和各种为第三方或客户代收的款项以外的各种收入。根据美国财务会计准则委员会（FASB）1980年在第3号财务会计概念公告(SFAC3）（企业财务报表的要素）（后为1985年发布的SFAC6所取代）的解释，综合收益是指“一个主体在某一期间与非业主方面进行交易或发生其他事项和情况所引起的权益（净资产）变动。它包括这一期间内除业主投资和派给业主款外，一切权益上的变动。”'},
     46: {'source_key': 'interest_income', 'save_key': 'int_inc', 'data_type': 'decimal(20,4)', 'comment': '利息收入\n利息收入是指纳税人购买各种债券等有价证券的利息，外单位欠款付给的利息以及其他利息收入。包括：购买各种债券等有价证券的利息，如购买国库券，重点企业建设债券、国家保值公债以及政府部门和企业发放的各类有价证券；企业各项存款所取得的利息外单位欠本企业款而取得的利息；其他利息收入等。'},
     47: {'source_key': 'premiums_earned', 'save_key': 'insur_prem_unearned', 'data_type': 'decimal(20,4)', 'comment': '已赚保费\n已赚保费是指保险起期已经预先缴付的保险费,过去的保险期间的保费就成为已赚的保费。'},
     48: {'source_key': 'commission_income', 'save_key': 'handling_chrg_comm_inc', 'data_type': 'decimal(20,4)', 'comment': '手续费及佣金收入\n手续费及佣金收入是指公司为客户办理各种业务收取的手续费及佣金收入，包括办理咨询业务、担保业务、代保管等代理业务以及办理投资业务等取得的手续费及佣金，如业务代办手续费收入、咨询服务收入、担保收入、资产管理收入、代保管收入，代理买卖证券、代理承销证券、代理兑付证券、代理保管证券等代理业务以及其他相关服务实现的手续费及佣金收入等。'},
     49: {'source_key': 'interest_expense', 'save_key': 'less_int_exp', 'data_type': 'decimal(20,4)', 'comment': '利息支出\n利息支出是指临时借款的利息支出。在以收付实现制作为记帐基础的前提条件下，所谓支出应以实际支付为标准，即资金流出，标志着现金、银行存款的减少。就利息支出而言、给个人帐户计息，其资金并没有流出，现金、银行存款并没有减少，因此，给个人计息不应作为利息支出列支。'},
     50: {'source_key': 'commission_expense', 'save_key': 'less_handling_chrg_comm_exp', 'data_type': 'decimal(20,4)', 'comment': '手续费及佣金支出\n手续费及佣金支出，本科目主要核算企业（金融）发生的与其经营活动相关的各项手续费、佣金等支出。'},
     51: {'source_key': 'refunded_premiums', 'save_key': 'prepay_surr', 'data_type': 'decimal(20,4)', 'comment': '退保金\n退保金是指公司经营的长期人身保险业务中，投保人办理退保时，按保险条款规定支付给投保人的金额。'},
     52: {'source_key': 'net_pay_insurance_claims', 'save_key': 'net_claim_exp', 'data_type': 'decimal(20,4)', 'comment': '赔付支出净额\n赔付支出主要指核算企业（保险）支付的原保险合同赔付款项和再保险合同赔付款项。企业（保险）可以单独设置“赔款支出”、“满期给付”、“年金给付”、“死伤医疗给付”、“分保赔付支出”等科目。可按保险合同和险种进行明细核算。'},
     53: {'source_key': 'withdraw_insurance_contract_reserve', 'save_key': 'chg_insur_cont_rsrv', 'data_type': 'decimal(20,4)', 'comment': '提取保险合同准备金净额\n保险准备金是指保险人为保证其如约履行保险赔偿或给付义务，根据政府有关法律规定或业务特定需要，从保费收入或盈余中提取的与其所承担的保险责任相对应的一定数量的基金。'},
     54: {'source_key': 'policy_dividend_payout', 'save_key': 'dvd_payable_insured', 'data_type': 'decimal(20,4)', 'comment': '保单红利支出\n保单红利支出是根据原保险合同的约定，按照分红保险产品的红利分配方法及有关精算结果而估算，支付给保单持有人的红利。'},
     55: {'source_key': 'reinsurance_cost', 'save_key': 'less_exp_recb_reinsurer', 'data_type': 'decimal(20,4)', 'comment': '分保费用\n分保费用，是办理初保业务的保险公司向其他保险公司分保保险业务，在向对方支付分保费的同时，向对方收取的一定费用，用以弥补初保人的费用支出。'},
     56: {'source_key': 'non_current_asset_disposed', 'save_key': 'loss_disp_noncur_asset', 'data_type': 'decimal(20,4)', 'comment': '非流动资产处置利得\n'},
     57: {'source_key': 'other_earnings', 'save_key': 'oth_inc', 'data_type': 'decimal(20,4)', 'comment': '其他收益\n'},
     58: {'source_key': 'asset_deal_income', 'save_key': 'asset_deal_inc', 'data_type': 'decimal(20,4)', 'comment': '资产处置收益\n'},
     59: {'source_key': 'sust_operate_net_profit', 'save_key': 'sust_operate_net_profit', 'data_type': 'decimal(20,4)', 'comment': '持续经营净利润\n'},
     60: {'source_key': 'discon_operate_net_profit', 'save_key': 'discon_operate_net_profit', 'data_type': 'decimal(20,4)', 'comment': '终止经营净利润\n'},
     61: {'source_key': 'credit_impairment_loss', 'save_key': 'credit_impairment_loss', 'data_type': 'decimal(20,4)', 'comment': '信用减值损失\n'},
     62: {'source_key': 'net_open_hedge_income', 'save_key': 'net_open_hedge_inc', 'data_type': 'decimal(20,4)', 'comment': '净敞口套期收益\n'},
     63: {'source_key': 'interest_cost_fin', 'save_key': 'fin_int_cost', 'data_type': 'decimal(20,4)', 'comment': '财务费用-利息费用\n'},
     64: {'source_key': 'interest_income_fin', 'save_key': 'fin_int_inc', 'data_type': 'decimal(20,4)', 'comment': '财务费用-利息收入\n'},
     65: {'source_key': 'rd_expenses', 'save_key': 'rd_exp', 'data_type': 'decimal(20,4)', 'comment': '研发费用\n'}}

class main():
    information = pd.DataFrame(df).T.dropna()
    params = {'table':'ashareincome', 
              'columns': {j['save_key'].upper(): j[2:].to_list() for i,j in information.iterrows()}, 
              'primary': 'UNIQUE_KEY', 
              'keys': ['ANN_DT', 'REPORT_PERIOD']}






