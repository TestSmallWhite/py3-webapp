#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from Field import Field
import logging

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):

        #因为不能修改Model，但是Model有显式使用ModelMetaclass类去创建，所以需要排除它
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        #获取表名字
        #__table__的值是user类的类属性，name是user类的名字，当类属性没有指定就获取类名
        tableName = attrs.get('__table__', None) or name

        #获取所有的Field和主键名:
        mappings = dict()   #保存关系
        fields = []         #保存非主键字段
        primaryKey = None   #标记主键

        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('found mapping: %s ==> %s' % (k, v))
                print('found mapping: %s ==> %s' % (k, v))

                mappings[k] = v

                if v.primary_key:
                    #找到主键：
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)

        if not primaryKey:
            raise RuntimeError('Primary key not found.')

        for k in mappings.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda f : '%s' %f, fields))

        #保存属性和列的映射关系
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName

        #主键属性名
        attrs['__primary_key__'] = primaryKey

        #除主键属性名
        attrs['__fields__'] = fields

        #构造默认的SELECT，INSERT， UPDATE， DELETE语句
        #廖雪峰的教程中，sql语句中，含有“`”，假如这里标错了，可能是这个原因，这里先不加上
        attrs['__select__'] = 'SELECT %s, %s FROM %s' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'INSERT INTO %s (%s, %s) VALUES(%s)'% (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        #attrs['__insert__'] = 'INSERT INTO %s (%s, %s) VALUES(%s)' % (tableName, ', '.join(escaped_fields), primaryKey, '11')
        attrs['__update__'] = 'UPDATE %s SET %s WHERE %s = ?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'DELETE FROM `%s` WHERE `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

def create_args_string(num):
    '''
    用来计算需要拼接多少个占位符
    :param num:
    :return:
    '''
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)