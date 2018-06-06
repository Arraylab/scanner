# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver


class RankManager:

    def __init__(self):
        self.driver = BuiltinDriver()

    def handle_rank_address(self):
        return self.driver.get_rank_address()
