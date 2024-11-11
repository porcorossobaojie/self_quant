# -*- coding: utf-8 -*-
# # 股票行情地址 token是每次请求必带的
# https://47.252.51.154:8443/v2/usa/stock/daily_price?token=d7ade34c386bde324f40b234fba3ef91
# # 指数行情地址
# https://47.252.51.154:8443/v2/usa/index/daily_price?token=d7ade34c386bde324f40b234fba3ef91
# 数据过滤
# 可以按照字段 symbol，trade_date过滤数据
# 支持操作 symbol__eq、symbol__lt、symbol__lte、symbol__gt、symbol__gte、symbol__in（这个效率比较低可以按天获取然后本地过滤）
# 		  trade_date__eq、trade_date__lt、trade_date__lte、trade_date__gt、trade_date__gte、trade_date__in
# 排序 trade_date__order=1 按照日期正序、trade_date__order=-1 按照日期倒序 按照symbol也可以
# 每次请求数据量默认是100条 通过字段size调整最大10000
# 返回字段可以通过 fields=xxx,xxx,xx 指定 例如 fields=symbol,adj_close,adj_open
import requests
import pandas as pd
token = 'd7ade34c386bde324f40b234fba3ef91'
quote_url = 'https://47.252.51.154:8443/v2/usa/stock/daily_price'
index_url = 'https://47.252.51.154:8443/v2/usa/index/daily_price'

# 示例
# 获取2023-03-01日的行情
params = {
    'token': token, #每次必填
    # 过滤数据
    'trade_date__eq': '2023-03-01',
    # 指定返回字段
    'fields': 'trade_date,symbol,adj_close,adj_volume',
    # 返回条数 每日行情数有几千行这里直接指定最大
    'size': 10000, # default 100
    # 排序
    'symbol__order': 1,
}
# 因为数据地址没有加网站证书 这里要指定 verify=False
res = requests.get(quote_url, params=params, verify=False)
quote = pd.DataFrame(res.json())
print(quote)
"""
      trade_date symbol  adj_close  adj_volume
0     2023-03-01      A   137.5100     3132400
1     2023-03-01     AA    51.5540     7613713
2     2023-03-01    AAC    10.2500      176651
3     2023-03-01   AACG     1.9292        8125
4     2023-03-01   AACI    10.0300        4812
...          ...    ...        ...         ...
5981  2023-03-01   ZVSA     2.1400       35557
5982  2023-03-01    ZWS    22.4000     1274600
5983  2023-03-01   ZYME     8.0100      494240
5984  2023-03-01   ZYNE     0.4629      306585
5985  2023-03-01   ZYXI    12.8500      205369

[5986 rows x 4 columns]
"""

# 获取 AAPL 2021-01-01 ~ 2023-03-01 行情
params = {
    'token': token, #每次必填
    # 过滤数据
    'symbol__eq': 'AAPL',
    # 日期过滤
    'trade_date__gte': '2021-01-01',
    'trade_date__lte': '2023-03-01',
    'size': 10000,
}
# 因为数据地址没有加网站证书 这里要指定 verify=False
res = requests.get(quote_url, params=params, verify=False)
quote = pd.DataFrame(res.json())
print(quote)
"""
    symbol  trade_date    open  ...   adj_low  adj_close  adj_volume
0     AAPL  2021-01-04  133.52  ...  125.0661   127.6807   145242741
1     AAPL  2021-01-05  128.89  ...  126.7138   129.2594    98987640
2     AAPL  2021-01-06  127.72  ...  124.6932   124.9083   157188462
3     AAPL  2021-01-07  128.36  ...  126.1514   129.1706   111062295
4     AAPL  2021-01-08  132.43  ...  128.4898   130.2855   106582432
..     ...         ...     ...  ...       ...        ...         ...
538   AAPL  2023-02-23  150.09  ...  147.2400   149.4000    48320300
539   AAPL  2023-02-24  147.11  ...  145.7200   146.7100    55221400
540   AAPL  2023-02-27  147.71  ...  147.4500   147.9200    44884700
541   AAPL  2023-02-28  147.05  ...  146.8300   147.4100    50350400
542   AAPL  2023-03-01  146.83  ...  145.0100   145.3100    55228900

[543 rows x 12 columns]
"""

# 指数行情 我们只保存了 SPX(S&P 500) 和 RUA （russell 3000）
# 获取 spx 2021-01-01 ~ 现在的行情

params = {
    'token': token,
    'symbol__eq': 'SPX',
    'trade_date__gte': '2021-01-01',
    'size': 10000,
}
res = requests.get(index_url, params=params, verify=False)
quote = pd.DataFrame(res.json())
print(quote)
"""
    symbol  trade_date     open     high      low    close      volume
0      SPX  2021-01-04  3764.61  3769.99  3662.71  3700.65  5006680000
1      SPX  2021-01-05  3698.02  3737.83  3695.07  3726.86  4582620000
2      SPX  2021-01-06  3712.20  3783.04  3705.34  3748.14  3171958843
3      SPX  2021-01-07  3764.71  3811.55  3764.71  3803.79  2571777491
4      SPX  2021-01-08  3815.05  3826.69  3783.60  3824.68  2381318227
..     ...         ...      ...      ...      ...      ...         ...
546    SPX  2023-03-07  4048.26  4050.00  3980.31  3986.37  3922500000
547    SPX  2023-03-08  3987.55  4000.41  3969.76  3992.01  3535570000
548    SPX  2023-03-09  3998.66  4017.81  3908.70  3918.32  4445260000
549    SPX  2023-03-10  3912.77  3934.05  3846.32  3861.59  5518190000
550    SPX  2023-03-13  3835.12  3905.05  3808.86  3855.76  4001022000

[551 rows x 7 columns]
"""
