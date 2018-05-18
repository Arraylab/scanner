# coding=utf-8
import time
from collector.log import Logger
from collector.agent.db_proxy import DbProxy
from collector.agent.fetcher import Fetcher
from tools import flags

FLAGS = flags.FLAGS


class DataAgent:
    ONE_MINUTE = 60

    def __init__(self):
        self.url_base = FLAGS.bytomd_rpc
        self.fetcher = Fetcher()
        self.proxy = DbProxy()
        self.height = self.proxy.get_height()
        self.logger = Logger('agent')
        self.logger.add_file_handler('agent.log')

    def request_genesis_block(self):
        genesis = self.fetcher.request_block(0)
        self.proxy.save_block(genesis)
        self.height = 0

    def sync(self):
        if self.height is None:
            self.request_genesis_block()

        self.roll_back()
        node_height = self.fetcher.request_chain_height()
        while self.height < node_height:
            node_block = self.fetcher.request_block(self.height + 1)
            pre_block_in_db = self.proxy.get_block_by_height(self.height)

            if node_block['previous_block_hash'] != pre_block_in_db['hash']:
                break

            self.proxy.save_block(node_block)
            self.height = node_block['height']

    def roll_back(self):
        self.proxy.remove_future_block()
        while self.height > 0:
            db_block = self.proxy.get_block_by_height(self.height)
            if db_block is not None:
                node_block = self.fetcher.request_block(self.height)
                if db_block['hash'] == node_block['hash']:
                    return

                self.proxy.remove_highest_block(db_block)

            self.proxy.set_height(self.height - 1)
            self.height -= 1

    def sync_forever(self):
        while True:
            self.sync()
            time.sleep(self.ONE_MINUTE)
