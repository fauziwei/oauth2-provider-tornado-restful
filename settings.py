# coding: utf-8
# Fauzi, fauziwei@yahoo.com
import os
import logging.config

basedir = os.path.abspath(os.path.dirname(__file__))

settings = {
	'redis_host': '127.0.0.1',
	'redis_port': 6379,
	'redis_db': 0,
	'debug': False
}

def config_logging():

	format = '[%(asctime)s] %(message)s'
	level = logging.DEBUG
	log_file = os.path.join(basedir, 'logs', 'debug')

	logging_settings = {
		'version': 1,
		'disable_existing_loggers': False,
		'handlers': {
			'console': {
				'class': 'logging.StreamHandler',
				'level': logging._levelNames[level],
				'formatter': 'file',
				'stream': 'ext://sys.stdout',
			},
			'file': {
				'class': 'logging.handlers.RotatingFileHandler',
				'level': 'DEBUG',
				'formatter': 'file',
				'filename': log_file,
				'mode': 'a',
				'maxBytes': 10485760,
				'backupCount': 5,
			},
		},
		'formatters': {
			'file': {
				'format': format
			}
		},
		'loggers': {
			'': {
				'level': 'DEBUG',
				'handlers': ['console', 'file']
			}
		}
	}

	logging.config.dictConfig(logging_settings)
	logging.captureWarnings(True)


config_logging()
