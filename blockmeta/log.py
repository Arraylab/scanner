#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from tools import flags
from logging.handlers import RotatingFileHandler

FLAGS = flags.FLAGS


def init_log(app):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s <%(name)s>: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join('.', FLAGS.DEBUG_LOG)
    debug_file_handler = RotatingFileHandler(debug_log, maxBytes=100000, backupCount=10)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    info_log = os.path.join('.', FLAGS.INFO_LOG)
    info_file_handler = RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    warn_log = os.path.join('.', FLAGS.WARN_LOG)
    warn_file_handler = RotatingFileHandler(warn_log, maxBytes=100000, backupCount=10)
    warn_file_handler.setLevel(logging.WARN)
    warn_file_handler.setFormatter(formatter)
    app.logger.addHandler(warn_file_handler)

    error_log = os.path.join('.', FLAGS.ERROR_LOG)
    error_file_handler = RotatingFileHandler(error_log, maxBytes=100000, backupCount=10)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    sh = logging.StreamHandler()
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter)
    app.logger.addHandler(sh)
