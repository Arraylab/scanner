#! /usr/bin/env python
# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver
from flask import current_app
from tools import flags

FLAGS = flags.FLAGS


class StatManager:
    """Manages the tx query"""
    def __init__(self):
        self.logger = current_app.logger
        self.driver = BuiltinDriver()

    def list_chain_stats(self):
        try:
            return self.driver.request_chain_status()
        except Exception, e:
            self.logger.error("StatManager.get_chain_status Error: %s" % str(e))
            raise Exception("get_chain_status error: %s", e)

    def list_node_stats(self):
        try:
            return self.driver.request_node_status()
        except Exception, e:
            self.logger.error("StatManager.get_node_status Error: %s" % str(e))
            raise Exception("get_node_status error: %s", e)
