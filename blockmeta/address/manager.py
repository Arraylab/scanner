# -*- coding: utf-8 -*-
from driver.bytom.builtin import BuiltinDriver
from flask import current_app
from tools import flags

FLAGS = flags.FLAGS


class AddressManager:
    def __init__(self):
        self.logger = current_app.logger
        self.driver = BuiltinDriver()

    def handle_address(self, addr, page=1):
        self.logger.info('handle address: %s' % str(addr))
        return self.driver.request_address_info(addr, page)
