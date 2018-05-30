from flask_cache import Cache
from flask import request
import urllib
redis_cli_config = {
	'CACHE_TYPE': 'redis',
	'CACHE_REDIS_HOST': '127.0.0.1',
	'CACHE_REDIS_PORT': 6379,
	'CACHE_REDIS_DB': '',
	'CACHE_REDIS_PASSWORD': ''
}
cache = Cache()


def cache_key():
	args = request.args
	key = request.path + '?' + urllib.urlencode([
		(k, v) for k in sorted(args) for v in sorted(args.getlist(k))
	])
	return key
