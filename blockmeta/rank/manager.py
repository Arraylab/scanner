# -*- coding: utf-8 -*-

from flask import current_app
from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class RankManager:

    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_rank_address(self):
        return self.driver.get_rank_address()
