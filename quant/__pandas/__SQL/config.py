# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:16:45 2020

@author: Porco Rosso
"""
'''
class __class():
    attrs = {'recommand': (str,),
             'charset': (str,),
             'port': (int,),
             'user': (str,),
             'password': (str,),
             'host': (str,),
             'pandasAttrName': (str,)}
    params = dict(zip(attrs.keys(), ['mysql+mysqlconnector://', 'utf8mb4', 3306, 'baojie', '123456', '127.0.0.1', 'SQL']))
'''    
class __class():
    params = {'recommand': 'mysql+pymysql://',
              'charset': 'utf8mb4', 
              'collate': 'utf8mb4_general_ci',
              'port': 3306, 
              'user': 'baojie', 
              'password': '123456', 
              'host': '127.0.0.1', 
              'schemas': ''}
    pandasAttrName = 'SQL'

class __obj():
    exec('pandasAttrName = __class.pandasAttrName')

bak = 'mysql+mysqlconnector://'

