# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import sys
import json
import logging
from functools import wraps

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

def access_token(f):
	@wraps(f)
	def wrapper(self, *args, **kwargs):
		_access_token = self.request.headers.get('Authorization', None)

		if _access_token is None:
			reason = u'access_token doesnt exist in request header Authorization.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return

		if not self.access_token_cache.exists(_access_token):
			reason = u'access_token doesnt exist in cache.'
			logger.debug(reason)
			self.finish( json.dumps({'success': False, 'reason': reason}) )
			return

		# get the access_token in redis.
		grant = self.access_token_cache.get_dict(_access_token)
		logger.debug('login: {}'.format(grant))

		self.user_id = grant['user_id']
		self.client_id = grant['client_id']
		self.grant_type = grant['grant_type']
		self.scope = grant['scope']

		return f(self, *args, **kwargs)

	return wrapper
