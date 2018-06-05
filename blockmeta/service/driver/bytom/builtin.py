# -*- coding: utf-8 -*-

from blockmeta.db.mongo import MongodbClient
from flask import current_app
from tools import flags, exception

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.logger = current_app.logger
        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def get_block_count(self):
        try:
            state = self.mongo_cli.get(FLAGS.db_status)
        except Exception as e:
            raise exception.DBError(e)
        return None if state is None else state[flags.FLAGS.block_height]

    def get_difficulty(self):
        try:
            height = self.get_block_count()
            difficulty = self.mongo_cli.get_one(table=FLAGS.block_info, cond={
                    FLAGS.block_height: height}, fields={'difficulty': 1, '_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return difficulty.get('difficulty', -1)

    def get_recent_award(self):
        height = self.get_block_count()
        if height < 0:
            return None
        s = height / 840000
        return 41250000000 / (s + 1)

    def get_last_block_interval(self):
        height = self.get_block_count()
        if height < 1:
            return None
        last_height = height - 1
        try:
            time = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: height}, fields={'timestamp': 1, '_id': 0})
            last_time = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: last_height}, fields={'timestamp': 1, '_id': 0})
            interval = time - last_time
        except Exception as e:
            raise exception.DBError(e)
        return interval

    def get_latest_block_miner(self):
        height = self.get_block_count()
        try:
            miner = self.mongo_cli.get_one(table=FLAGS.block_info, cond={FLAGS.block_height: height}, fields={'miner': 1, '_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return miner

    def get_total_tx_num(self):
        try:
            total_num = self.mongo_cli.count(FLAGS.transaction_info)
        except Exception as e:
            raise exception.DBError(e)
        return total_num

    def get_total_addr_num(self):
        try:
            total_num = self.mongo_cli.count(FLAGS.address_info)
        except Exception as e:
            raise exception.DBError(e)
        return total_num

    def get_total_btm(self):
        init_btm = 140700041250000000
        init_award = 41250000000
        epoch_length = 840000
        current_height = self.get_block_count()
        epoch = current_height // epoch_length

        total_num = 0
        for n in range(epoch + 1):
            award = init_award / (n + 1)
            total_num += award * (current_height - n * epoch_length)

        total_num += init_btm
        return total_num

    def get_block_by_height(self, height):
        try:
            block_info = self.mongo_cli.get_one(
                table=FLAGS.block_info, cond={
                    FLAGS.block_height: int(height)}, fields={'_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return block_info

    def get_block_by_hash(self, hash):
        try:
            block_info = self.mongo_cli.get_one(
                table=FLAGS.block_info, cond={
                    FLAGS.block_id: hash}, fields={'_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return block_info

    def get_tx_by_hash(self, hash):
        try:
            tx_info = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: hash}, fields={'_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return tx_info

    def get_info_by_addr(self, address):
        try:
            info = self.mongo_cli.get_one(table=FLAGS.address_info, cond={FLAGS.address: address}, fields={'_id': 0})
        except Exception as e:
            raise exception.DBError(e)
        return info
