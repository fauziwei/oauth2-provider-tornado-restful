# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import sys
import json
import uuid
import base64
import hashlib
import logging
from tornado import gen
from base.handlers import BaseHandler
from lib.decorator import access_token

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

# ------------------------------------------------
class Index(BaseHandler):
	'''Index.'''
	pass


# ------------------------------------------------
class Role(BaseHandler):
	'''Role.'''

	# GET
	@gen.coroutine
	@access_token
	def get(self, *args, **kwargs):
		role_id = self.get_argument('role_id', None)
		# if role_id is None then query all roles
		roles = yield self.get_pool(role_id)
		self.write( json.dumps({'roles': roles}) )

	@gen.coroutine
	def get_pool(self, role_id):
		roles = self.get_roles(role_id)
		raise gen.Return(roles)

	# POST
	@gen.coroutine
	@access_token
	def post(self, *args, **kwargs):
		name = self.get_argument('name', None)
		success = yield self.post_pool(name)
		self.write( json.dumps({'success': success}) )		

	@gen.coroutine
	def post_pool(self, name):
		success = self.create_role(name)
		raise gen.Return(success)


# ------------------------------------------------
class User(BaseHandler):
	'''User.'''

	# GET
	@gen.coroutine
	@access_token
	def get(self, *args, **kwargs):
		user_id = self.get_argument('user_id', None)
		# if user_id is None then query all users
		users = yield self.get_pool(user_id)
		self.write( json.dumps({'users': users}) )

	@gen.coroutine
	def get_pool(self, user_id):
		users = self.get_users(user_id)
		raise gen.Return(users)

	# POST
	@gen.coroutine
	@access_token
	def post(self, *args, **kwargs):
		email = self.get_argument('email', None)
		password = self.get_argument('password', None)
		role_id = self.get_argument('role_id', None)
		success = yield self.post_pool(email, password, role_id)
		self.write( json.dumps({'success': success}) )		

	@gen.coroutine
	def post_pool(self, email, password, role_id):
		success = self.create_user(email, password, role_id)
		raise gen.Return(success)


# ------------------------------------------------
class Client(BaseHandler):
	'''Client App.'''

	# GET
	@gen.coroutine
	@access_token
	def get(self, *args, **kwargs):
		client_id = self.get_argument('client_id', None)
		# if client_id is None then query all clients
		clients = yield self.get_pool(client_id)
		self.write( json.dumps({'clients': clients}) )

	@gen.coroutine
	def get_pool(self, client_id):
		clients = self.get_clients(client_id)
		raise gen.Return(clients)

	# POST
	@gen.coroutine
	@access_token
	def post(self, *args, **kwargs):
		name = self.get_argument('name', None)
		success = yield self.post_pool(name)
		self.write( json.dumps({'success': success}) )

	@gen.coroutine
	def post_pool(self, name):
		success = self.create_client(name)
		raise gen.Return(success)


# ------------------------------------------------
class Oauth2(BaseHandler):
	'''Request token.'''

	# GET
	@gen.coroutine
	def get(self):
		# check headers.
		headers = self.request.headers.get('Authorization', None)
		if headers is None or not headers.startswith('Basic '):
			reason = u'Request token oauth2, incorrect base64.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return

		try:
			decoded = base64.decodestring(headers[6:])
			client_id, client_secret = decoded.split(':', 2)
		except:
			reason = u'Request token oauth2, exception during headers decoding.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return

		session = self.models.Db().Session()
		client = session.query(self.models.Client).filter_by(id=client_id, secret=client_secret).first()
		if not client:
			self.commit(session)
			reason = u'Request token oauth2, incorrect client_id/client_secret.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return
		self.commit(session)

		# check body
		email = self.get_argument('email', None)
		password = self.get_argument('password', None)
		grant_type = self.get_argument('grant_type', None)
		scope = self.get_argument('scope', None)

		if email is None or password is None:
			reason = u'Request token oauth2, required email and password.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return

		session = self.models.Db().Session()
		user = session.query(self.models.User).filter_by(email=email, password=hashlib.sha1(password).hexdigest()).first()
		if not user:
			self.commit(session)
			reason = u'Request token oauth2, user doesnt exist.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return
		user_id = user.id
		self.commit(session)

		_ = True
		while _:
			_access_token = str(uuid.uuid4())
			grant = self.access_token_cache.exists(_access_token)
			if not grant:
				_ = False
		grant = {
			'user_id': user_id,
			'client_id': client_id,
			'grant_type': grant_type,
			'scope': scope
		}
		self.access_token_cache.save_dict(_access_token, grant)
		# 1 day expire
		expire = 86400
		self.access_token_cache.expire(_access_token, expire)
		self.finish( json.dumps({
			'success': True,
			'access_token': _access_token,
			'expire': expire,
			'redirect_uri': [ # available urls in this site which can be accessed by access_token
				'http://localhost:4000/role/',
				'http://localhost:4000/user/',
				'http://localhost:4000/client/'
			]
		}) )
