# -*- coding: utf-8 -*-

from driver.bytom.builtin import BuiltinDriver
from flask import current_app


class ServiceManager(object):

    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_chain_api(self, query):
        try:
            # if query == 'getdifficulty':
            #     return self.driver.get_difficulty()
            if query == 'getblockcount':
                return self.driver.get_block_count()
            if query == 'reward':
                return self.driver.get_reward()
            if query == 'chainsize':
                return self.driver.get_chain_size()
            if query == 'totalbtc':
                return self.driver.get_totalbtc()
            if query == 'interval':
                return self.driver.get_block_avg_time()
            if query == 'hashrate':
                return self.driver.get_nethash()
            if query == 'avgtxnum':
                return self.driver.get_avg_tx_num()
            if query == 'nextdifficulty':
                return self.driver.get_next_difficulty()
            if query == 'lastminer':
                return self.driver.get_last_miner()
            if query == 'lastblockhash':
                return self.driver.get_last_blockhash()
            if query == 'unconfirmedcount':
                return self.driver.get_uncomfirmed_txs()
            if query == '24hrpoolstat':
                return self.driver.get_mining_pool_stat()
            if query == '24hrblockcount':
                return self.driver.get_block_count_in_range()
            if query == 'ticker':
                return self.driver.get_ticker()
        except Exception, e:
            self.logger.error("BitcoinAPIManager.handle_chain_api Error: %s" % str(e))
            raise Exception("handle_chain_api error: %s", e)
