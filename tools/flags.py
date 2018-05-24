# -*- coding: utf-8 -*-

import gflags
FLAGS = gflags.FLAGS


# agent
# bytomd RPC
gflags.DEFINE_string('bytomd_rpc', 'http://localhost:9888', '')
gflags.DEFINE_string('get_block', 'get-block', '')
gflags.DEFINE_string('get_block_height_arg', 'block_height', '')
gflags.DEFINE_string('get_block_count', 'get-block-count', '')
gflags.DEFINE_string('tx_i_id', 'spent_output_id', '')
gflags.DEFINE_string('tx_o_id', 'id', '')
gflags.DEFINE_string('get_hash_rate', 'get-hash-rate', '')
gflags.DEFINE_string('decode_program', 'decode-program', '')

gflags.DEFINE_bool('MONGODB_ENABLE', True, 'switch')
gflags.DEFINE_string('mongo_bytom_host', '127.0.0.1', 'mongodb host')
gflags.DEFINE_string('mongo_bytom_port',  27017, 'mongodb port')

# bytomd db
gflags.DEFINE_string('mongo_bytom', 'bytom', 'mongodb bytom main db')
gflags.DEFINE_string('mongodb_user', 'bytom', 'mongodb user name')
gflags.DEFINE_string('mongodb_password', 'bytom', 'mongodb user password')
gflags.DEFINE_integer('table_capacity', 99000000, 'table capacity')

# bytom table
gflags.DEFINE_string('db_status', 'status', '')
gflags.DEFINE_string('address_info', 'address_info', '')
gflags.DEFINE_string('block_info', 'block_info', '')
gflags.DEFINE_string('transaction_info', 'transaction_info', '')
gflags.DEFINE_string('asset_info', 'asset_info', '')


# bytom table attributes
gflags.DEFINE_string('block_height', 'height', '')
gflags.DEFINE_string('coinbase', 'coinbase', '')
gflags.DEFINE_string('block_count', 'block_count', '')
gflags.DEFINE_string('address', 'address', '')
gflags.DEFINE_string('asset_id', 'asset_id', '')
gflags.DEFINE_string('block_id', 'hash', '')
gflags.DEFINE_string('previous_block_hash', 'previous_block_hash', '')
gflags.DEFINE_string('merkle_root', 'transaction_merkle_root', '')
gflags.DEFINE_string('nonce', 'nonce', '')
gflags.DEFINE_string('timestamp', 'timestamp', '')
gflags.DEFINE_string('difficulty', 'difficulty', '')
gflags.DEFINE_string('block_nbit', 'bits', '')
gflags.DEFINE_string('block_size', 'size', '')
gflags.DEFINE_string('transaction_status_hash', 'transaction_status_hash', '')


gflags.DEFINE_string('transactions', 'transactions', '')
gflags.DEFINE_string('transaction_in', 'inputs', '')
gflags.DEFINE_string('transaction_out', 'outputs', '')
gflags.DEFINE_string('amount', 'amount', '')
gflags.DEFINE_string('tx_io_type', 'type', '')
gflags.DEFINE_string('tx_id', 'id', '')
gflags.DEFINE_string('is_tx_in', 'is_tx_in', '')
gflags.DEFINE_string('data', 'data', '')
gflags.DEFINE_string('tx_io_id', 'tx_io_id', '')
gflags.DEFINE_string('size', 'size', '')
gflags.DEFINE_string('tx_fee', 'fee', '')


gflags.DEFINE_string('version', 'version', '')

# log.py
gflags.DEFINE_string('DEBUG_LOG', 'logs/debug.log.py', 'location')
gflags.DEFINE_string('ERROR_LOG', 'logs/error.log.py', 'location')
gflags.DEFINE_string('INFO_LOG', 'logs/info.log.py', 'location')
gflags.DEFINE_string('WARN_LOG', 'logs/warn.log.py', 'location')
