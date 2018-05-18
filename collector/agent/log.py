import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, app):
        self.logger = logging.getLogger(app)
        self.logger.setLevel(logging.DEBUG)
        self.fmt = logging.Formatter(
            '%(asctime)s %(levelname)s <%(name)s>: %(message)s '
            '[in %(pathname)s:%(lineno)d]')
        self.app = app

    def add_stream_handler(self, clevel = logging.DEBUG):
        sh = logging.StreamHandler()
        sh.setLevel(clevel)
        sh.setFormatter(self.fmt)
        self.logger.addHandler(sh)

    def add_file_handler(self, file_name=None, flevel=logging.DEBUG):
        file_name = self.app if file_name is None else file_name
        if not os.path.exists('./logs/'):
            os.mkdir('./logs/')
        log_path = os.path.join('./logs', '%s.log' % file_name)
        fh = RotatingFileHandler(log_path, maxBytes=100000, backupCount=10)
        fh.setLevel(flevel)
        fh.setFormatter(self.fmt)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


# if __name__ == '__main__':
#     logyyx = Logger('test')
#     logyyx.add_stream_handler()
#     logyyx.add_file_handler('my_log_name')
#     logyyx.debug('a bug message')
#     logyyx.info('an info message')
#     logyyx.warn('a warning message')
#     logyyx.error('a error message')
#     logyyx.cri('a critical message')
