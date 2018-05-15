# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class OdinManager:
    def __init__(self):
        self.driver = BuiltinDriver()

    def handle_odin(self, attribute,  content):
        return self.driver.request(attribute, content)
