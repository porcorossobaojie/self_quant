= r'\((\w+)\): Linear'3# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:46:31 2024

@author: admin
"""

import datasets
import pandas as pd
"""
# datasets.load_dataset
要用代理
"""
"""
# datasets.load_from_desk
报错
"""


# 对于本地文件，用pandas做一次数据转换
# 再用 datasets.Dataset.from_pandas
df = pd.read_json('f:\\LLM\\datasets\\Orion-zhen-dpo-ruozhiba-emoji\\rouzhiba_dpo_emoji.json')
data_obj =  datasets.Dataset.from_pandas(df)



