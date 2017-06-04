# coding: utf-8
# Fauzi, fauziwei@yahoo.com
from tornado.web import url
from handlers import Index, Role, User, Client, Oauth2

url_patterns = [
	url(r'/', Index, name='index, not applicable yet'),
	url(r'/role/', Role, name='get/post role'),
	url(r'/user/', User, name='get/post user'),
	url(r'/client/', Client, name='get/post client'),
	url(r'/oauth2/', Oauth2, name='get request token'),
]
