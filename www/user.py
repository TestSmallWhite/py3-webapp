#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
设计ORM需要从上层调用者角度来设计

我们先考虑如何定义一个User对象，然后把数据库表users和它关联起来。
"""

from Field import IntegerField, StringField
from Model import Model

class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()

if __name__ == '__main__':
    user = User(id=111, name='Michael')
    print(user)
