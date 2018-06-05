# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver
from flask import current_app
from blockmeta.utils.bytom import check_block_info, is_address, is_hash_prefix


class ServiceManager(object):

    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_chain_api(self, query):
        if query == 'getdifficulty':
            return self.driver.get_difficulty()
        if query == 'getblockcount':
            return self.driver.get_block_count()
        if query == 'reward':
            return self.driver.get_recent_award()
        if query == 'lastinterval':
            return self.driver.get_last_block_interval()
        if query == 'lastminer':
            return self.driver.get_latest_block_miner()
        if query == 'totalbtm':
            return self.driver.get_total_btm()
        if query == 'totaltxnum':
            return self.driver.get_total_tx_num()
        if query == 'totaladdrnum':
            return self.driver.get_total_addr_num()
        else:
            raise Exception('No such Chain api')

    def handle_block_api(self, api_info, query):
        tag = check_block_info(api_info)
        if not tag:
            raise Exception("Invalid Parameter: %s" % api_info)

        if query == 'info':
            if tag == 'HASH':
                return self.driver.get_block_by_hash(tag)
            else:
                return self.driver.get_block_by_height(tag)
        else:
            raise Exception('No such Block api')

    def handle_tx_api(self, api_info, query):
        if not is_hash_prefix(api_info):
            raise Exception("Not a valid transaction hash %s" % api_info)
        if query == 'info':
            return self.driver.get_tx_by_hash(api_info)
        else:
            raise Exception('No such tx api')

    def handle_address_api(self, api_info, query):
        if not is_address(api_info):
            raise Exception("Not a valid address %s" % api_info)
        if query == 'info':
            return self.driver.get_info_by_addr(api_info)
        else:
            raise Exception('No such address api')
