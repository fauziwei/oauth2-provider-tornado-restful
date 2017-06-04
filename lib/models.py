# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import sys
from sqlalchemy import Column, Table, String, DateTime
from sqlalchemy import ForeignKey, MetaData, create_engine
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm  import sessionmaker, relationship
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine('sqlite:///sqlite.db', encoding='utf8', poolclass=NullPool, echo=False)
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)

class Db(object):

	def __init__(self):
		self.Session = sessionmaker()
		self.Session.configure(bind=engine)

	@property
	def session(self):
		return self.Session()


class Role(Base):
	__tablename__ = 'role'
	__table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
	id = Column('id', String(36), primary_key=True)
	name = Column('name', String(100), index=True)


class User(Base):
	__tablename__ = 'user'
	__table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
	id = Column('id', String(36), primary_key=True)
	email = Column('email', String(100), index=True)
	password = Column('password', String(40), index=True)
	role_id = Column('role_id', String(36), ForeignKey('role.id'), index=True)

	role = relationship('Role')


class Client(Base):
	'''1 App can have multiple owner.'''
	__tablename__ = 'client'
	__table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
	id = Column('id', String(36), primary_key=True)
	secret = Column('secret', String(36), nullable=False, index=True)
	name = Column('name', String(100), nullable=False, unique=True, index=True)


# class Grant(Base):
# 	__tablename__ = 'grant'
# 	__table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
# 	id = Column('id', String(36), primary_key=True)
# 	user_id = Column('user_id', String(36), ForeignKey('user.id'), index=True)
# 	client_id = Column('client_id', String(36), ForeignKey('client.id'), index=True)
# 	type = Column('type', String(40), index=True)
# 	redirect_uri = Column('redirect_uri', TEXT())
# 	access_token = Column('access_token', String(36), index=True)
# 	refresh_token = Column('refresh_token', String(36), index=True)
# 	expires = Column('expires', DateTime)
# 	scope = Column('scope', TEXT())

# 	user = relationship('User')
# 	client = relationship('Client')


Base.metadata.create_all(engine)
