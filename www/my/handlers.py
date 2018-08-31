#!/usr/bin/env python3
# -*- coding: utf-8 -*-


' url handlers '


from webframe import get, post
from models import User, Blog, Comment
import time


@get('/')
def index(request):
	summary = '成长，是一段渐行渐远的分离。'
	blogs = [
		Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
		Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
		Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
	]
	return {
		'__template__': 'test.html',
		'blogs': blogs
	}