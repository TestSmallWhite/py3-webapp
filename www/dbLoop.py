#!/usr/bin/env python3
# -*- coding:utf-8 -*-



"""
创建一个全局的连接池，每个HTTP请求都可以从连接池中直接获取数据库连接。使用连接池的好处是不必频繁地打开和关闭数据库连接，而是能复用就尽量复用
"""

# class dbLoop(object):
#
#     #创建全局的连接池
#     async def creat_Pool( **kw):
#         logging.info("create database connection pool...")
#
#         loop2 = asyncio.get_event_loop()
#
#         return await aiomysql.create_pool(
#             #dict.get()方法 == dict[]，但是get方法可以在找不到对应的key时返回一个指定的values
#             host = kw.get('host', 'localhost'),
#             port = kw.get('prot', 3306),
#
#             #登录的用户名指定一个默认值
#             #user = kw['user'],
#             user = kw.get('user', 'root'),
#
#             # 登录的密码指定一个默认值
#             #password = kw['password'],
#             password = kw.get('password','123456'),
#
#             #db = kw['db'],
#             db = kw.get('db', 'awesome'),
#             charset = kw.get('charset','utf8'),
#             autocommit = kw.get('autocommit', True),
#             maxsize = kw.get('maxsize', 10),
#             minsize = kw.get('minsize', 1),
#             loop = loop2
#         )


"""
利用@contextmanager装饰器去自动打开连接池，当执行完毕sql语句后，又自动关闭
"""

import asyncio
import aiomysql
import logging
from contextlib import contextmanager


class db_pool():
    """
    要使用with关键词实现功能，需要重写3个方法，分别是__init__, __enter__, __exit__
    但是使用@contextmanager后就不需要重写了

    代码的执行顺序是：
	1. with语句首先执行yield之前的语句，因此打印出<h1>；
	2. yield调用会执行with语句内部的所有语句，因此打印出hello和world；
	3. 最后执行yield之后的语句，打印出</h1>。
    """

    @contextmanager
    async def creat_pool(cls, **kw):
        #第一步，先连接上连接池
        #获取协程
        loop = asyncio.get_event_loop()

        #带引log
        logging.info("create database connection pool...")

        pool = await aiomysql.create_pool(
            #dict.get()方法 == dict[]，但是get方法可以在找不到对应的key时返回一个指定的values
            host = kw.get('host', 'localhost'),
            port = kw.get('prot', 3306),

            #登录的用户名指定一个默认值
            #user = kw['user'],
            user = kw.get('user', 'root'),

            # 登录的密码指定一个默认值
            #password = kw['password'],
            password = kw.get('password','123456'),

            #db = kw['db'],
            db = kw.get('db', 'awesome'),
            charset = kw.get('charset','utf8'),
            autocommit = kw.get('autocommit', True),
            maxsize = kw.get('maxsize', 10),
            minsize = kw.get('minsize', 1),
            loop = loop
        )

        yield
        #执行with下面的代码

        #执行with下面的代码完毕
        #关闭连接池
        pool.close()
        await pool.wait_closed()