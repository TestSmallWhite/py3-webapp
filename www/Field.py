#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
定义数据库字段类型
"""

class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' %(self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name = None, primary_key = False, default = None, ddl = 'VARCHAR(100)'):
        super(StringField, self).__init__(name, ddl, primary_key, default)


class IntegerField(Field):
    def __init__(self, name = None, primary_key = False, default = 0, ddl = 'INT(4)'):
        super(IntegerField, self).__init__(name, ddl, primary_key, default)


class CharField(Field):
    def __init__(self, name = None, primary_key = False, default = None, ddl = 'CHAR(11)'):
        super(CharField, self).__init__(name, ddl, primary_key, default)

class BooleanField(Field):
    def __init__(self,name = None, primary_key = False, default = False, ddl = 'BOOLEAN'):
        super(BooleanField, self).__init__(name, ddl, primary_key, default)

class TextField(Field):
    def __init__(self,name = None, primary_key = False, default = None, ddl = 'MEDIUMTEXT'):
        super(TextField, self).__init__(name, ddl, primary_key, default)

class FloatField(Field):
    def __init__(self,name = None, primary_key = False, default = 0.0, ddl = 'REAL'):
        super(FloatField, self).__init__(name, ddl, primary_key, default)