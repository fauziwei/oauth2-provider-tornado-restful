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

# --------------------------------------------------------
# Initial configuration

session = Db().Session()

# Role
role = Role()
role.id = 'dbd67d8a-d8d9-41e6-bade-6352110a479a'
role.name = 'administrator'
session.add(role)
session.commit()

role = Role()
role.id = '5c171ff9-2be8-43ac-b4ee-ee0decfdc4db'
role.name = 'staff'
session.add(role)
session.commit()

# User
user = User()
user.id = '7329d1e5-edd4-4d04-8ea8-090ee72ed880 '
user.email = 'admin@yy.com'
user.password = 'd033e22ae348aeb5660fc2140aec35850c4da997' # admin
user.role_id = 'dbd67d8a-d8d9-41e6-bade-6352110a479a'
session.add(user)
session.commit()

user = User()
user.id = 'ef81661f-069e-42a4-839e-602ca473dff4'
user.email = 'xxx@cc.com'
user.password = 'b60d121b438a380c343d5ec3c2037564b82ffef3' # xxx
user.role_id = '5c171ff9-2be8-43ac-b4ee-ee0decfdc4db'
session.add(user)
session.commit()

# Client
client = Client()
client.id = 'c310174d-2839-4b41-b1fa-f750f8c04fe6'
client.secret = 'd32b4e7c-51ac-4f99-8e16-739c0ac8a668'
client.name = 'production_tool'
session.add(client)
session.commit()

session.close()

print('Finish.')
