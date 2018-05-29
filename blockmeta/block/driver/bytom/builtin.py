# -*- coding: utf-8 -*-

from flask import current_app

from blockmeta.db.mongo import MongodbClient
from blockmeta.utils.bytom import is_hash_prefix, remove_0x
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

    def request_block_info(self, arg):
        try:
            hash_or_height = remove_0x(arg)
            is_hash = len(hash_or_height) == 64
            return self.get_block_by_hash(hash_or_height) if is_hash else self.get_block_by_height(hash_or_height)
        except Exception, e:
            self.logger.error("Block.BuiltinDriver.request_block_info Error: %s" % str(e))
            raise Exception("request_block_info error: %s", e)

    def list_blocks(self, start, end):
        try:
            block_list = []
            blocks = self.get_block_latest_in_range(start, end)
            for block in blocks:
                block_info = self._show_block(block)
                block_list.append(block_info)
            total_num = self._get_total_num()

            return block_list, total_num
        except Exception as e:
            self.logger.error("Block.BuiltinDriver.list_blocks Error: %s" % str(e))
            raise Exception("list_blocks error: %s", e)

    def get_block_by_height(self, height):
        try:
            if int(height) < 0:
                raise Exception("Block height is wrong!")
            block = self.mongo_cli.get_one(
                table=FLAGS.block_info, cond={
                    FLAGS.block_height: int(height)})
            if block is None:
                raise Exception("Block not found!")
            block_info = self._show_block(block)

        except Exception as e:
            raise exception.DBError(e)
        return block_info

    def get_block_by_hash(self, blockhash):
        try:
            if not is_hash_prefix(blockhash):
                raise Exception("Block hash is wrong!")
            block = self.mongo_cli.get_one(
                table=FLAGS.block_info, cond={
                    FLAGS.block_id: blockhash})
            if block is None:
                raise Exception("Block not found!")
            block_info = self._show_block(block)
        except Exception as e:
            raise exception.DBError(e)
        return block_info

    def get_block_latest_in_range(self, start, end):
        try:
            blocks = self.mongo_cli.get_many(
                table=FLAGS.block_info,
                n=end-start,
                sort_key=FLAGS.block_height,
                ascend=False,
                skip=start)
        except Exception as e:
            raise exception.DBError(e)
        return blocks

    def _show_block(self, block):
        '''
        format conversion
        convert to the block message that user see
        :param block: block from db
        :return:
        '''
        block_height = block.get(FLAGS.block_height)
        block_hash = block.get(FLAGS.block_id)
        block_version = block.get(FLAGS.version)
        pre_block_hash = block.get(FLAGS.previous_block_hash)
        tx_merkle_root = block.get(FLAGS.merkle_root)
        nonce = block.get(FLAGS.nonce)
        timestamp = block.get(FLAGS.timestamp)
        difficulty = block.get(FLAGS.difficulty)
        nbit = block.get(FLAGS.block_nbit)
        transactions = block.get(FLAGS.transactions)
        block_size = block.get(FLAGS.block_size)
        transaction_status_hash = block.get(FLAGS.transaction_status_hash)

        block_info = {
            'block_height': block_height,
            'block_hash': block_hash,
            'block_version': block_version,
            'pre_block_hash': pre_block_hash,
            'tx_merkle_root': tx_merkle_root,
            'nonce': nonce,
            'timestamp': timestamp,
            'difficulty': difficulty,
            'nbit': nbit,
            'transactions': transactions,
            'block_size': block_size,
            'transaction_status_hash': transaction_status_hash
        }
        return block_info

    def _get_total_num(self):
        state = self.mongo_cli.get(flags.FLAGS.db_status)
        return 0 if state is None else state[flags.FLAGS.block_height]
