# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class AddressManager:
    def __init__(self):
        self.driver = BuiltinDriver()

    def handle_address(self, addr, page=1):
        return self.driver.request_address_info(addr, page)
