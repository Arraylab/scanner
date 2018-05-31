# -*- coding: utf-8 -*-

import sys

from blockmeta import urls, log
from flask import Flask
from redis_cli_conf import redis_cli_config, cache
from tools import flags


FLAGS = flags.FLAGS
FLAGS(sys.argv)
DEFAULT_APP_NAME = 'btmscan'


def configure_modules(app):
    urls.register_api(app)


def configure_logging(app):
    log.init_log(app)


def configure_cache(app, cache):
    app.config.from_object(redis_cli_config)
    cache.init_app(app, redis_cli_config)


def create_app():
    app = Flask(DEFAULT_APP_NAME, static_folder='static', static_url_path='')
    # register log.py
    configure_logging(app)
    # register rest url
    configure_modules(app)
    # configure cache
    configure_cache(app, cache)
    return app


app = create_app()
