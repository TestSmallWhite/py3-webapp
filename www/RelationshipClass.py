#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
设计ORM需要从上层调用者角度来设计

这是一个关系类，用于每个class都对应一张表
每个类的属性都对应着每张表中的字段定义
"""

from Field import IntegerField, StringField, BooleanField, FloatField, TextField
from Model import Model
import time,uuid

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key = True, default = next_id, ddl = 'VARCHAR(50)')
    email = StringField(ddl = 'VARCHAR(50)')
    passwd = StringField(ddl = 'VARCHAR(50)')
    admin = BooleanField()
    name = StringField(ddl = 'VARCHAR(50)')
    image = StringField(ddl = 'VARCHAR(500)')
    create_at = FloatField(default = time.time)

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField(ddl = 'TEXT')
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField(ddl = 'TEXT')
    created_at = FloatField(default=time.time)

