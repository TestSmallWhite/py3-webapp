#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, inspect, logging, functools

from urllib import parse
from aiohttp import web
from apis import APIError

#@get装饰器，给处理get请求的函数绑定url和http method-get的属性
def get(path):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

#@post装饰器，和get装饰器一样，但是给函数绑定属性
def post(path):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

#检查处理函数是不是有request请求参数，返回布尔值，如果有request参数，检查该参数是否为函数的最后一个参数，如果不是就报错
def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters   #返回一个dict，含有参数名，参数值
    for name, param in params.items():
        if name == 'request':
            found = True
            continue    #找到后就退出本次循环

        #如果找到‘request’参数后，还出现其他参数，就抛出异常
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY
                      and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError('request parameter must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
    return found

#检查函数是否有关键字参数集，返回布尔值
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters

    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True


#检查函数是否有命名关键字参数，返回布尔值
def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters

    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

#将函数所有的命名关键字参数名作为一个tuple返回
def get_name_kw_args(fn):

    #为什么要使用list？
    #因为tuple不可以增删元素，但是又要返回一个tuple，所以使用tuple包裹一个list
    args = []

    params = inspect.signature(fn).parameters

    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

#将函数所有没有默认值的命名关键字参数名作为一个tuple返回
def get_required_kw_args(fn):
    args = []

    #An ordered mapping of parameters' names to the corresponding Parameter object.
    params = inspect.signature(fn).parameters

    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.defalut == inspect.Parameter.empty
            # param.kind : describes how argument values are bound to the parameter.
            # KEYWORD_ONLY : value must be supplied as keyword argument, which appear after a * or *args
            # param.default : the default value for the parameter,if has no default value,this is set to Parameter.empty
            # Parameter.empty : a special class-level marker to specify absence of default values and annotations
            args.append(name)
    return tuple(args)

#这个类用来处理请求，封装处理函数
class RequestHandler(object):
    def __init__(self, app, fn):
        # app : an application instance for registering the fn
        # fn : a request handler with a particular HTTP method and path
        self.__app = app
        self.__func = fn
        self.__has_request_arg = has_request_arg(fn)    #检查函数是否有request参数
        self.__has_var_kw_arg = has_var_kw_arg(fn)  # 检查函数是否有关键字参数集
        self.__has.named_kw_args = has_named_kw_args(fn) # 检查函数是否有命名关键字参数
        self.__named_kw_args = get_name_kw_args(fn) # 将函数所有的 命名关键字参数名 作为一个tuple返回
        self.required_kw_args = get_required_kw_args(fn)    # 将函数所有 没默认值的 命名关键字参数名 作为一个tuple返回

    async def __call__(self, request):
        #分析请求，request handler,must be a coroutine that accepts a request instance as its only argument and returns a streamresponse derived instance
        kw = None

        # 当传入的处理函数具有 关键字参数集 或 命名关键字参数 或 request参数
        if self.__has_var_kw_arg or self.__has.name_kw_args or self.required_kw_args:
            if request.method == 'POST':
                #POST请求预处理
                if not request.content_type:
                    #无正文类型信息时返回
                    return web.HTTPBadRequest('Missing Content-Type')
                ct = request.content_type.lower()







