# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import redis
import redis.exceptions

class Cache(object):
	__slots__ = ('rds', 'host', 'port', 'db')

	def __init__(self, *args, **kwargs):
		self.rds = redis.StrictRedis(
			host=kwargs['host'], port=kwargs['port'], db=kwargs['db']
		)

	def expire(self, key, ttl):
		# ttl in second
		self.rds.expire(key, ttl)

	def save(self, key, value):
		self.rds.set(key, value)

	def get(self, key):
		return self.rds.get(key)

	def delete(self, key):
		try:
			self.rds.delete(key)
		except redis.exceptions.ResponseError:
			pass

	def keys(self, key=None):
		# get all keys or key with input
		if key is None:
			return self.rds.keys()
		return self.rds.keys(key)

	def exists(self, key):
		# return True/False
		return self.rds.exists(key)

	def save_dict(self, key, value):
		self.rds.hmset(key, value)

	def get_dict(self, key):
		return self.rds.hgetall(key)
