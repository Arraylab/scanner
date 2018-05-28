# -*- coding: utf-8 -*-

from flask import current_app

from blockmeta.constant import DEFAULT_OFFSET
from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class BlockManager:
    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_block(self, block_id):
        try:
            return self.driver.request_block_info(block_id)
        except Exception, e:
            self.logger.error("BlockManager.handle_block Error: %s" % str(e))
            raise Exception("handle_block error: %s", e)

    def list_blocks(self, start, end):
        blocks = {}
        result, total_num = self.driver.list_blocks(start, end)
        blocks['pages'] = total_num / DEFAULT_OFFSET + 1
        blocks['blocks'] = result
        return blocks


