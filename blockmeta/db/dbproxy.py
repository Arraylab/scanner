# -*- coding: utf-8 -*-

from mongo import MongodbClient
from tools import exception, flags

FLAGS = flags.FLAGS


class MongoProxy(object):

    def __init__(self):
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    '''
        table information, including address, block, transaction etc.
    '''
    def get_address_info(self, address):
        addr_info = self.mongo_cli.get_one(table=FLAGS.address_info, cond={FLAGS.address: address}, fields={'_id': 0})
        return addr_info

    def get_block_info(self, b_id):
        if isinstance(id, int):
            block_info = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: b_id}, fields={'_id': 0})
        else:
            block_info = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_id: b_id}, fields={'_id': 0})
        return block_info

    def get_tx_info(self, tx_hash):
        tx_info = self.mongo_cli.get_one(table=FLAGS.transaction_info, cond={FLAGS.tx_id: tx_hash}, fields={'_id': 0})
        return tx_info

    '''
        misc, about block, transaction and address 
    '''
    def get_recent_height(self):
        try:
            state = self.mongo_cli.get(flags.FLAGS.db_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if state is None else state[flags.FLAGS.block_height]

    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})

    def get_block_hash_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height}, fields={'hash': 1, '_id': 0})

    def get_difficulty(self):
        try:
            height = self.get_recent_height()
            difficulty = self.mongo_cli.get_one(FLAGS.block_info, {'height': height}, fields={'difficulty': 1, '_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return difficulty.get('difficulty')

    def get_difficulty_by_height(self, height):
        try:
            difficulty = self.mongo_cli.get_one(FLAGS.block_info, {'height': height}, fields={'difficulty': 1, '_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return difficulty.get('difficulty')

    def get_latest_block_miner(self):
        height = self.get_recent_height()
        try:
            miner = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: height}, fields={'miner': 1, '_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return miner.get('miner')

    def get_recent_award(self):
        height = self.get_recent_height()
        if height < 0:
            return None
        s = height / 840000
        return 41250000000 / (s + 1)

    def get_last_block_interval(self):
        height = self.get_recent_height()
        if height < 1:
            return None
        last_height = height - 1
        try:
            time = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: height}, fields={'timestamp': 1, '_id': 0})
            last_time = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: last_height}, fields={'timestamp': 1, '_id': 0})
            interval = time.get('timestamp') - last_time.get('timestamp')
        except Exception as e:
            raise exception.DBError(e)
        return interval


    '''
        total number of address and transaction
    '''
    def get_total_tx_num(self):
        total_num = self.mongo_cli.count(FLAGS.transaction_info)
        return total_num

    def get_total_addr_num(self):
        total_num = self.mongo_cli.count(FLAGS.address_info)
        return total_num

    '''
        scope, range by block height
    '''
    def get_hash_rate_in_range(self, start, end):
        try:
            hash_rates = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                items={"hash_rate": 1, "_id": 0},
                n=end-start,
                skip=start)
        except Exception as e:
            raise exception.DBError(e)
        return hash_rates

    def get_timestamps_in_range(self, start, end):
        try:
            timestamps = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                items={"timestamp": 1, "_id": 0},
                n=end-start,
                sort_key='timestamp',
                ascend=True,
                skip=start)
        except Exception as e:
            raise exception.DBError(e)
        return timestamps

    def get_transactions_in_range(self, low, high):
        try:
            coinbase = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                items={"transactions": 1, "_id": 0},
                n=high - low,
                skip=low)
        except Exception as e:
            raise exception.DBError(e)
        return coinbase

    '''
        stats of chain & node
    '''
    def get_chain_stats_list(self):
        try:
            stats = self.mongo_cli.get_many(table=FLAGS.chain_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if stats is None else stats

    def get_node_stats_list(self):
        try:
            stats = self.mongo_cli.get_many(table=FLAGS.node_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if stats is None else stats

    def request_node_status(self):
        try:
            stats = self.mongo_cli.get_many(
                table=FLAGS.node_status,
                n=1,
                sort_key=FLAGS.timestamp,
                ascend=False
            )
        except Exception as e:
            raise exception.DBError(e)
        return stats

