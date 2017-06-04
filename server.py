# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import logging
from tornado import web, ioloop, httpserver
from urls import url_patterns
from settings import settings
import lib.cache as cache
import lib.models as models

logger = logging.getLogger(__name__)

class Application(web.Application):
	access_token_cache = cache.Cache(
		host=settings.get('redis_host'),
		port=settings.get('redis_port'),
		db=settings.get('redis_db')
	)
	models = models

	def __init__(self):
		super(Application, self).__init__(url_patterns, **settings)

def main():
	address, port = '127.0.0.1', 4000
	app = Application()
	server = httpserver.HTTPServer(app)
	server.listen(port, address=address)
	logger.debug('Oauth2 Server running on: {}'.format(port))
	ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()
