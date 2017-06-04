# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import sys
import uuid
import hashlib
import logging
import traceback
from tornado import web

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

class BaseHandler(web.RequestHandler):

	def __init__(self, *args, **kwargs):
		super(BaseHandler, self).__init__(*args, **kwargs)

	@property
	def access_token_cache(self):
		return self.application.access_token_cache

	@property
	def models(self):
		return self.application.models

	def commit(self, session):
		try:
			session.flush()
			session.commit()
			success = True
		except:
			traceback.print_exc()
			session.rollback()
			success = False
		finally:
			session.close()
		return success

	def create_id_from_table(self, table):
		session = self.models.Db().Session()
		_ = True
		while _:
			_id = str(uuid.uuid4())
			obj = session.query(table).filter_by(id=_id).first()
			if not obj:
				_ = False
		self.commit(session)
		return _id


	''' ----- Role ----- '''

	def get_roles(self, role_id):
		session = self.models.Db().Session()
		if role_id is None:
			roles = session.query(self.models.Role).order_by(self.models.Role.name).all()
		else:
			role = session.query(self.models.Role).filter_by(id=role_id).first()
			roles = []
			roles.append(role)

		_roles = []
		iterator = iter(roles)
		while True:
			try:
				role = next(iterator)
				d = {'id': role.id, 'name': role.name}
				_roles.append(d)
			except StopIteration:
				break
		self.commit(session)
		return _roles

	def create_role(self, name):
		session = self.models.Db().Session()
		role = session.query(self.models.Role).filter_by(name=name).first()
		if role:
			self.commit(session)
			return False
		self.commit(session)
		
		role_id = self.create_id_from_table(self.models.Role)
		session = self.models.Db().Session()
		role = self.models.Role()
		role.id = role_id
		role.name = name
		session.add(role)
		return self.commit(session)


	''' ----- User ----- '''

	def get_users(self, user_id):
		session = self.models.Db().Session()
		if user_id is None:
			# roles_users = session.query(self.models.Role, self.models.User).join(
			# 	self.models.User).filter(
			# 	self.models.Role.id==self.models.User.role_id).order_by(
			# 	self.models.User.email).all()
			roles_users = session.query(self.models.Role, self.models.User).filter(
				self.models.Role.id==self.models.User.role_id).order_by(
				self.models.User.email).all()

			_users = []
			iterator = iter(roles_users)
			while True:
				try:
					role, user = next(iterator)
					d = {
						'id': user.id,
						'email': user.email,
						'password': user.password,
						'role_id': user.role_id,
						'role_name': role.name
					}
					_users.append(d)
				except StopIteration:
					break
			self.commit(session)
			return _users

		else:
			role_user = session.query(self.models.Role, self.models.User).join(
				self.models.User).filter(
				self.models.User.id==user_id).filter(
				self.models.Role.id==self.models.User.role_id).first()
			if role_user:
				role, user = role_user
				d = {
					'id': user.id,
					'email': user.email,
					'password': user.password,
					'role_id': user.role_id,
					'role_name': role.name
				}
				_users = []
				_users.append(d)
				self.commit(session)
				return _users

			self.commit(session)
			return []

	def create_user(self, email, password, role_id):
		session = self.models.Db().Session()
		user = session.query(self.models.User).filter_by(email=email).first()
		if user:
			self.commit(session)
			return False
		self.commit(session)

		user_id = self.create_id_from_table(self.models.User)
		session = self.models.Db().Session()
		user = self.models.User()
		user.id = user_id
		user.email = email
		user.password = hashlib.sha1(password).hexdigest()
		user.role_id = role_id
		session.add(user)
		return self.commit(session)


	''' ----- Client ----- '''

	def get_clients(self, client_id):
		session = self.models.Db().Session()
		if client_id is None:
			clients = session.query(self.models.Client).order_by(self.models.Client.name).all()
			_clients = []
			iterator = iter(clients)
			while True:
				try:
					client = next(iterator)
					d = {
						'id': client.id,
						'secret': client.secret,
						'name': client.name
					}
					_clients.append(d)
				except StopIteration:
					break
			self.commit(session)
			return _clients

		else:
			client = session.query(self.models.Client).filter_by(id=client_id).first()
			if client:
				d = {
					'id': client.id,
					'secret': client.secret,
					'name': client.name
				}
				_clients = []
				_clients.append(d)
				self.commit(session)
				return _clients

			self.commit(session)
			return []

	def create_client(self, name):
		session = self.models.Db().Session()
		client = session.query(self.models.Client).filter_by(name=name).first()
		if client:
			self.commit(session)
			return False
		self.commit(session)

		client_id = self.create_id_from_table(self.models.Client)
		session = self.models.Db().Session()
		client = self.models.Client()
		client.id = client_id
		client.secret = str(uuid.uuid4())
		client.name = name
		session.add(client)
		return self.commit(session)
