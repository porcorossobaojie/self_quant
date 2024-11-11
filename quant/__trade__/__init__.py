# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 08:46:50 2022

@author: Porco Rosso

"""

import pandas as pd
from __trade__.main.main import DataFrame, Series

pd._DataFrame = DataFrame
pd._Series = Series

if pd.Timestamp.today().month == 14 and pd.Timestamp.today().day == 14:
    print('''    今天 我在这里记录历史

    上海 因为新冠疫情的原因 封城已经近一个月的时间
    
    我不知道 有多少老人 因为封城得不到救助 默默的忍受病痛乃至死去
    
    我不知道 有多少婴儿 因为封城买不到食物 
    
    我不知道 多少父亲母亲 因为封城即将失去工作 还背负着巨额的房贷
    
    我不知道 有多少“灵活就业”的人 因为封城 舍不得买昂贵的配送食物 每天只吃一顿稀饭
    
    我只知道 市民热线无法打通 120急救已经是满负荷运转
    
    我只知道 无数的反应人们真实生活的文章、录音、影像 因为“违反相关的法律法规 不予以显示”
    
    我只知道 为了一个至今感染近三十万人 重症一例的疾病 我们像傻子一样的重复着核酸、抗原的检测
    
    我只知道 本来 今天是鲍杰和秦升美登记结婚的日子 
    ''')








