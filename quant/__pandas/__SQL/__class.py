# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 09:37:32 2021

@author: Porco Rosso
"""

from numpy import ndarray, isreal
from datetime import datetime
import pandas as pd
import pymysql
from sqlalchemy import create_engine

from __pandas.__SQL.config import __class as config

class _login(type('_login', (), config.params)):
    '''
    ===========================================================================
    
    ------------
    Explain:
    ------------
        <class> provide functions for reading datas from MySQL and something else.
        here are the attributes, functions that Unit does.
    
    ---------------------------------------------------------------------------

    ------------
    Attributes:                
    ------------
        one instance object has following attributes(it might not but looks like) 
    for desecribing or working.
    
            user:
                str.
                the value of MySQL db's user name if needed in functions.
                
            password:
                str.
                the value of MySQL db's password if needed in functions.
            host:
                str.
                the value of MySQL db's host if needed in functions.
    
            charset:
                str.
                the value of MySQL db's charset if needed in functions.
                
            port:
                int.
                the value of MySQL db's port if needed in functions.
                
            loginfo:
                dict.
                the values of current login information, only read.
                
    ---------------------------------------------------------------------------
    '''
    __internal_attrs__ =  list(config.params.keys())
    def __init__(self, **kwargs):
        '''
        ------------
        
        Explain:
            set any attributes in user, password, host, charset, port if needed.
            
        ------------

        Parameters:
            
            user, password, host, charset, port which has explained in <class>'s
        attributes.
        
        ------------
        
        Returns:
            /
            
        ------------

        '''
        
        self.__internal_attrs__ = list(set(self.__internal_attrs__) | set(kwargs.keys()))
        [setattr(self, i, j) for i,j in kwargs.items()]
        
    def __call__(self, replace=False, **kwargs):
        '''
        ------------
        
        Explain:
            exchange params for connecting MySQL.
            
        ------------

        Parameters:
            
            all parameters will use its recommand value when instance object builded
        if not given.
        
            user, password, host, charset, port which has explained in <class>'s
        attributes.
        
            schemas: 
                str.
                MySQL schemas name.

        ------------
        
        Returns:
            /
        
        ------------
        '''
        params = {i: getattr(self, i) for i in self.__internal_attrs__}
        params.update(kwargs)
        if replace:
            return self.__class__(**params)
        else:
            [setattr(self, i, j) for i, j in params.items()]
    
    def __engine__(self, **kwargs):
        '''
        ------------
        
        Explain:
            create engine for connecting MySQL by parameters.
            
        ------------

        Parameters:
            
            all parameters will use its recommand value when instance object builded
        if not given.
        
            user, password, host, charset, port which has explained in <class>'s
        attributes.
        
            schemas: 
                str.
                MySQL schemas name.

        ------------
        
        Returns:
            engine object.
        
        ------------
        '''
        params = {i: getattr(self, i) for i in self.__internal_attrs__}
        params.update(kwargs)
        return create_engine(
                             params['recommand'] + 
                             params['user'] + 
                             ':' + 
                             params['password'] + 
                             '@' + 
                             params['host'] + 
                             ':' + 
                             params['port'].__str__() + 
                             '/' + 
                             params['schemas'] + 
                             '?charset=' + 
                             params['charset'])
    
    def __read__(self, schemas=None, table=None, columns=None, where=None, chunksize=64000000, log=False, **kwargs):
        '''
        ------------
        
        Explain:
            read MySQL datas by parameters.
            
        ------------
        
        Parameters:
            
            schemas:
                str.
                MySQL schemas name.
                
            table:
                str.
                MySQL table name.
                
            columns:
                str or list.
                column names for reading if needed.
                z`
            where:
                str.
                filter condition assign to MySQL 'where'.
            
            chunksize:
                int.
                whether read MySQL database by chunksize.
                
            kwargs:
                user, password, host, charset, port if needed.

        ------------

        Returns:
            dataframe.
                
        ------------            
        '''
        schemas = getattr(self, 'schemas', schemas) if schemas is None else schemas
        table = getattr(self, 'table', table) if table is None else table
        columns = getattr(self, 'columns', columns) if columns is None else (columns.keys() if isinstance(columns, dict) else columns)
        columns = '*' if columns is None else columns
        where = getattr(self, 'where', where) if where is None else where
        where = None if where == '' else where
        columns = ','.join(map(lambda x: x.__str__(), columns)) if not isinstance(columns, str) else columns
        command = 'SELECT ' + columns + ' FROM ' + schemas + '.' + table if where is None else 'SELECT ' + columns + ' FROM ' + schemas + '.' + table + ' WHERE ' + where
        if log:
            print(command)
        if chunksize is not None:
            offset = 0
            x = []
            while True:
                order = command + (' LIMIT %s OFFSET %s' %(chunksize, offset))
                obj = pd.read_sql(order,  con=self.__engine__(**kwargs, schemas=schemas))
                x.append(obj)
                if len(obj) < chunksize:
                    break
                else:
                    offset += chunksize
            x = pd.concat(x)
        else:
            x = pd.read_sql(command, con=self.__engine__(**kwargs, schemas=schemas))
        return x
    
    @property
    def __login_info__(self):
        return {i: getattr(self, i) for i in self.__internal_attrs__}
    
    def __exist__(self, schemas=None, table=None):
        '''
        ------------
        
        Explain:
            check whether exist schemas.table or not.
        
        ------------
        
        Parameters

            schemas:
                str.
                MySQL schemas name.
                
            table:
                str.
                MySQL table name.

        ------------

        Returns:
            bool.
                
        ------------            

        '''
        schemas = getattr(self, 'schemas', schemas) if schemas is None else schemas
        table = getattr(self, 'table', table) if table is None else table
        x = self.__command__('select * from information_schema.tables where table_name = "%s" and table_schema = "%s"' %(table, schemas), schemas)
        return bool(x)
        
    
    def __create__(self, schemas=None, table=None, columns=None, primary=None, keys=None, partition=None, charset=None, collate=None, log=False, **kwargs):
        '''
        ------------
        
        Explain:
            generate MySQL command by parameters and create table.
        
        ------------
        
        Parameters:
            
            schemas:
                str.
                MySQL schemas name.

            table: 
                str.
                table name.
                
            columns:
                str or list.
                columns name.
            
            primary:
                str.
                primary key name if needed.
                
            keys: 
                list.
                keys names if needed.
                
            partition:
                list.
                partition information if needed
                
            charset:
                str.
                charset information if needed.
                
            collate:
                str.
                collate information if needed.
                
            log:
                bool.
                whether pirnt SQL command or not.
                
        ------------

        Returns:
            /
        
        ------------
        '''
        schemas = getattr(self, 'schemas', schemas) if schemas is None else schemas
        table = getattr(self, 'table', table) if table is None else table
        columns = getattr(self, 'columns', columns) if columns is None else columns
        primary = getattr(self, 'primary', primary) if primary is None else primary
        keys = getattr(self, 'keys', keys) if keys is None else keys
        partition = getattr(self, 'partition', partition) if partition is None else partition
        charset = getattr(self, 'charset', charset) if charset is None else charset
        collate = getattr(self, 'collate', collate) if collate is None else charset.__str__() + '_general_ci'
        
        tableCommand = 'CREATE TABLE `%s` (\n' %(table)
        if primary is not None:
            if partition is None:
                pri = '`%s` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,' %(primary)
            else:
                pri = '%s INT NOT NULL AUTO_INCREMENT, UNIQUE KEY (%s, %s),' %(primary, primary, list(partition.keys())[0])
            tableCommand += pri
        if isinstance(columns, dict):
            cols = ',\n'.join(['`%s` %s DEFAULT NULL COMMENT "%s"' %(i, j[0], (j[1] if len(j) > 1 else '')) for i,j in columns.items()])
        else:
            cols = ',\n'.join(['`%s` %s DEFAULT NULL COMMENT "%s"' %(i[0], i[1], (i[2] if len(i) > 2 else '')) for i in columns])
        if keys is not None:
            ks = ',\n' + ',\n'.join(['key (%s)' %(i) if isinstance(i, str) else 'key(%s)' %(','.join(i)) for i in keys])
        else:
            ks = ''
        command = tableCommand + cols + ks + ')\n ENGINE = InnoDB DEFAULT CHARSET = %s COLLATE=%s' %(charset, collate)
        if partition is not None:
            part = '\n PARTITION BY RANGE COLUMNS(%s)(\n' %(list(partition.keys())[0])
            rang = ['PARTITION p%s VALUES LESS THAN ("%s")' %(i, j) if not isreal(j) or isinstance(j, datetime) else 'PARTITION p%s VALUES LESS THAN (%s)' %(i, j) for i,j in enumerate(list(partition.values())[0])]
            rang = ',\n'.join(rang)
            part = part + rang + ')'
            command += part
        if log:
            print(command)
        self.__command__(command, schemas, **kwargs)

    def __command__(self, command, schemas=None, **kwargs):
        '''
        ------------
        
        Explain:
            run MySQL command.
        
        -----------
        
        Parameters:
            
            command:
                str.
                MySQL command.
                
            schemas:
                str.
                value of schemas command did in.
                
            kwargs:
                user, password, host, port, charset if needed.
        
        ------------
        
        Returns:
            /
            
        ------------
        '''
        params = {i: getattr(self, i) for i in self.__internal_attrs__}
        params.update(kwargs)
        schemas = getattr(self, 'schemas', schemas) if schemas is None else schemas
        con = pymysql.connect(host = params['host'], 
                              port = params['port'], 
                              user = params['user'], 
                              password = params['password'],
                              charset = params['charset'],
                              db = schemas)
        cur = con.cursor()
        x = cur.execute(command)
        x = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return x
    
    def __schemas_info__(self, **kwargs):
        '''
        ------------
        
        Explian:
            getting MySQL schemas informations.
            
        ------------
        
        Returns:
            dataframe.
            
        ------------
        '''
        params = {'columns': '*', 'where': ''}
        params.update(kwargs)
        x = self.__read__('information_schema', 'columns', **params)
        return x
    
def __sweet__(words):
    import time
    for item in words.split():
        print('\n'.join([''.join([(item[(x-y) % len(item)] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(12, -12, -1)]))
        time.sleep(1.5)

class __class():
    login = _login()
    read = login.__read__
    command = login.__command__
    create = login.__create__
    exist = login.__exist__
    info = login.__schemas_info__
    __login__ = _login
    
setattr(pd, config.pandasAttrName, __class)


