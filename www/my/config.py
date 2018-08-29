#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
Configuration
'''

import config_defaullt

class Dict(dict):
	'增加字典调用方式, a.b'
	def __init__(self, names=(), values=(), **kw):
		super().__init__(**kw)

		for k, v in zip(names, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

#覆盖方法，不断对比开发配置和生产环境配置，如果发生不一样，把生产环境配置的键值覆盖开发环境配置
def merge(defaluts, override):
	r = {}
	for k, v in defaluts.items():
		if k in override:
			if isinstance(v, dict):
				r[k] = merge(v, override[k])
		else:
			r[k] = v
	return r

def toDict(d):
	#转换成Dict类
	D = Dict()
	for k, v in d.items:
		D[k] = toDict(v) if isinstance(v, dict) else v
		return D

configs = config_defaullt.configs
try:
	import config_override
	configs = merge(configs, config_override.configs)
except ImportError:
	raise AttributeError(r"import error:%s" % ('config_override.configs'))
configs = toDict(configs)

