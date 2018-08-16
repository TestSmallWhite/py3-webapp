#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import asyncio
import logging
import dbLoop
import aiomysql
from ModelMetaclass import ModelMetaclass
import Field
from dbLoop import dbLoop

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model object has no attribute '%s" %(key))

    def __setattr__(self, key, value):
        self[key] = value

    def log(cls,sql, args=()):
        logging.info('SQL: %s' % sql)

    def getValue(self,key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)

        if value is None:
            field = self.__mappings__[key]

            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)

        return value


    async def select(self, sql, args,size = None):
        Model.log(None, sql,args)
        global __pool

        with (await dbLoop.creat_Pool(None)) as conn:
            cur = await conn.cursor(aiomysql.DictCursor)
            await cur.execute(sql.replace('?', '&s'), args or ())

            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
            await cur.close()
            logging.info('rows returned: %s' % len(rs))
            return rs

    async def execute(self, sql, args):
        Model.log(None, sql)
        global __pool

        with (await __pool) as conn:
            try:
                cur = await conn.cursor()
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
                await cur.close()
            except BaseException as e:
                raise
            return affected

    @classmethod
    async def find(cls,pk):
        logging.info(' find object by primary key. ')

        rs = await Model.select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await Model.execute(None, self.__insert__, args)
        if rows !=1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

        print('sava finish')
