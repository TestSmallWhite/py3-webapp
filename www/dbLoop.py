#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio
import aiomysql
import logging

"""
创建一个全局的连接池，每个HTTP请求都可以从连接池中直接获取数据库连接。使用连接池的好处是不必频繁地打开和关闭数据库连接，而是能复用就尽量复用
"""

class dbLoop(object):
    #创建全局的连接池
    async def creat_Pool(loop, **kw):
        logging.info("create database connection pool...")

        global __pool

        __pool = await aiomysql.create_pool(
            #dict.get()方法 == dict[]，但是get方法可以在找不到对应的key时返回一个指定的values
            host = kw.get('host', 'localhost'),
            port = kw.get('prot', 3306),

            #登录的用户名指定一个默认值
            #user = kw['user'],
            user = kw.get('user', 'root'),

            # 登录的密码指定一个默认值
            #password = kw['password'],
            password = kw.get('password',123456),

            db = kw['db'],
            charset = kw.get('charset','utf8'),
            autocommit = kw.get('autocommit', True),
            maxsize = kw.get('maxsize', 10),
            minsize = kw.get('minsize', 1),
            loop = loop
        )