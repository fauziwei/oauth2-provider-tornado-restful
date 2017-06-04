# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import redis
import redis.exceptions

class Cache(object):

	def __init__(self, host='127.0.0.1', port=6379, db=0):
		self.rds = redis.StrictRedis(host=host, port=port, db=db)

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
