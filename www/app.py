#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging; logging.basicConfig(level = logging.INFO)
import asyncio, os, json, time

from datetime import datetime

from aiohttp import web

def index(request):
    return web.Response(body='<h1>Awesome</h1>'.encode(), content_type='text/html')

@asyncio.coroutine
def init(loop):
    #把循环对象传入，启动监听
    app = web.Application(loop = loop)

    #根据不同请求，处理不同返回
    #这里是一个GTE请求获取首页的数据，第一个参数应该是请求类型，第二个是地址，第三个是返回对应处理的函数
    app.router.add_route('GET', '/', index)

    #初始化监听
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)

    #输出logging
    logging.info("server started at http://127.0.0.1:9000...")

    return srv

#获取循环对象
loop = asyncio.get_event_loop()

#初始化循环
loop.run_until_complete(init(loop))

#启动循环
loop.run_forever()

