#! /usr/bin/env python
# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver
from flask import current_app
from tools import flags

FLAGS = flags.FLAGS


class StatManager(object):
    """Manages the tx query"""
    def __init__(self):
        self.logger = current_app.logger
        self.driver = BuiltinDriver()

    def list_chain_stats(self):
        self.logger.info('list chain stats')
        return self.driver.request_chain_status()

    def list_node_stats(self):
        self.logger.info('list node stats')
        return self.driver.request_node_status()
