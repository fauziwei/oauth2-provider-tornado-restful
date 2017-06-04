# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import os
import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm  import sessionmaker, mapper
from sqlalchemy.pool import NullPool

reload(sys)
sys.setdefaultencoding('utf-8')

database = 'sqlite.db'
engine = create_engine('sqlite:///%s' % database, encoding='utf8', poolclass=NullPool, echo=False)

class Db(object):
	'''Session applicable.'''

	def __init__(self):
		self.Session = sessionmaker()
		self.Session.configure(bind=engine)

	@property
	def session(self):
		return self.Session()

metadata = MetaData(bind=engine)

class Role(object): pass
class User(object): pass
class Client(object): pass

role_table = Table('role', metadata, autoload=True)
user_table = Table('user', metadata, autoload=True)
client_table = Table('client', metadata, autoload=True)

mapper(Role, role_table)
mapper(User, user_table)
mapper(Client, client_table)


# Query
session = Db().Session()

print(50 * '_')
print('Table: role')
# roles = session.query(Role).limit(1)
roles = session.query(Role).all()
for role in roles:
	print(role.id, role.name)

print(50 * '_')
print('Table: user')
# users = session.query(User).limit(1)
users = session.query(User).all()
for user in users:
	print(user.id, user.email, user.password, user.role_id)

print(50 * '_')
print('Table: client')
# clients = session.query(Client).limit(1)
clients = session.query(Client).all()
for client in clients:
	print('id: {0}'.format(client.id))
	print('secret: {0}'.format(client.secret))
	print('name: {0}'.format(client.name))

session.close()
