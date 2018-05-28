#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
import os
import flags
import logging
from logging.handlers import RotatingFileHandler

FLAGS = flags.FLAGS


def init_log(owner):
    logger = logging.getLogger(owner)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s <%(name)s>: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_log = os.path.join('.', FLAGS.DEBUG_LOG)

    debug_file_handler = RotatingFileHandler(debug_log, maxBytes=100000, backupCount=10)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    logger.addHandler(debug_file_handler)

    error_log = os.path.join('.', FLAGS.ERROR_LOG)
    error_file_handler = RotatingFileHandler(error_log, maxBytes=100000, backupCount=10)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    error_log = os.path.join('.', FLAGS.INFO_LOG)
    error_file_handler = RotatingFileHandler(error_log, maxBytes=100000, backupCount=10)
    error_file_handler.setLevel(logging.INFO)
    error_file_handler.setFormatter(formatter)
    logger.addHandler(error_file_handler)

    sh = logging.StreamHandler()
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger
