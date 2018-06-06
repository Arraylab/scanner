# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler


def init_log(app):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s <%(name)s>: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    log_dir = os.getcwd() + '/logs/'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_path = os.path.join(log_dir, '%s.log' % app.name)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    fh = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=10)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    app.logger.addHandler(sh)
    app.logger.addHandler(fh)
