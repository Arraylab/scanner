from collector.log import Logger
from collector.db.mongodriver import MongodbClient
from tools import flags


class DbProxy:
    btm_id = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

    def __init__(self):
        self.url_base = flags.FLAGS.bytomd_rpc
        self.logger = Logger('dbproxy')
        self.logger.add_file_handler('dbproxy.log')
        self.mongo_cli = MongodbClient(host=flags.FLAGS.mongo_bytom_host, port=flags.FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(flags.FLAGS.mongo_bytom)

    def get_height(self):
        state = self.mongo_cli.get(flags.FLAGS.db_status)
        return None if state is None else state[flags.FLAGS.block_height]

    def set_height(self, height):
        self.mongo_cli.update_one(flags.FLAGS.db_status, {}, {'$set': {flags.FLAGS.block_height: height}}, True)

    def save_block(self, block):
        # if block['height'] == 538:
        #     raise Exception
        self.mongo_cli.insert(flags.FLAGS.block_info, block)

        transactions = []
        for transaction in block['transactions']:
            transaction.update({'block_height': block['height'], 'block_hash': block['hash']})
            transactions.append(transaction)
        self.mongo_cli.insert_many(flags.FLAGS.transaction_info, transactions)
        self.index_address(block)
        self.update_asset_status(block)
        self.set_height(block['height'])

    def index_address(self, block):
        address_dict = {}
        for transaction in block['transactions']:
            for tx_input in transaction['inputs']:
                if tx_input['type'] != 'spend' or tx_input.get('asset_id').lower() != self.btm_id:
                    continue

                address = tx_input.get('address', None)
                if address is None:
                    continue
                address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                         {'address': address})
                if address_info is None:
                    raise Exception('transaction input address not existed in address collection: %s', address)

                address_info['balance'] -= tx_input['amount']
                address_info['sent'] += tx_input['amount']
                txs_set = set(address_info['txs'])
                if transaction['id'] not in txs_set:
                    address_info['txs'].append(transaction['id'])
                address_dict[address] = address_info

            for tx_output in transaction['outputs']:
                if tx_output.get('type') != 'control' or tx_output.get('asset_id').lower() != self.btm_id:
                    continue

                address = tx_output.get('address')
                if not address:
                    continue

                address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                         {'address': address})
                if address_info is None:
                    address_info = {
                        'address': address,
                        'balance': 0,
                        'recv': 0,
                        'sent': 0,
                        'txs': [],
                    }
                address_info['balance'] += tx_output['amount']
                address_info['recv'] += tx_output['amount']
                txs_set = set(address_info['txs'])
                if transaction['id'] not in txs_set:
                    address_info['txs'].append(transaction['id'])

                address_dict[address] = address_info

        for address in address_dict:
            address_dict[address].update({'block_hash': block['hash'], 'block_height': block['height']})
        self.save_address_info(address_dict)

    def update_asset_status(self, block):
        asset_dict = {}
        for transaction in block['transactions']:
            if transaction['status_fail']:
                continue

            for tx_input in transaction['inputs']:
                if tx_input.get('asset_id').lower() != self.btm_id:
                    if tx_input['type'] == 'issue':
                        asset_dict[tx_input['asset_id']] = {
                            'asset_id': tx_input['asset_id'],
                            'asset_definition': tx_input['asset_definition'],
                            'amount': tx_input['amount'],
                            'retire': 0,
                            'issue_by': transaction['id'],
                            'txs': [transaction['id']],
                            'balances': {}
                        }
                    elif tx_input['type'] == 'spend':
                        asset_info = asset_dict.get(tx_input['asset_id'], None) or self.mongo_cli.get_one(
                            flags.FLAGS.asset_info, {'asset_id': tx_input['asset_id']})
                        if 'address' not in tx_input:
                            continue

                        asset_info['balances'][tx_input['address']] -= tx_input['amount']
                        tx_set = set(asset_info['txs'])
                        if transaction['id'] not in tx_set:
                            asset_info['txs'].append(transaction['id'])
                        asset_dict[tx_input['asset_id']] = asset_info

                    else:
                        continue
            for tx_output in transaction['outputs']:
                if tx_output.get('asset_id').lower() != self.btm_id:
                    if tx_output['type'] == 'control':
                        asset_info = asset_dict.get(tx_output['asset_id'], None) or self.mongo_cli.get_one(
                            flags.FLAGS.asset_info, {'asset_id': tx_output['asset_id']})
                        if 'address' not in tx_output:
                            continue

                        if tx_output['address'] not in asset_info['balances']:
                            asset_info['balances'][tx_output['address']] = 0
                        asset_info['balances'][tx_output['address']] += tx_output['amount']
                        tx_set = set(asset_info['txs'])
                        if transaction['id'] not in tx_set:
                            asset_info['txs'].append(transaction['id'])
                        asset_dict[tx_output['asset_id']] = asset_info
                    elif tx_output['type'] == 'retire':
                        asset_info = asset_dict.get(tx_output['asset_id'], None) or self.mongo_cli.get_one(
                            flags.FLAGS.asset_info, {'asset_id': tx_output['asset_id']})
                        asset_info['retire'] += tx_output['amount']
                        tx_set = set(asset_info['txs'])
                        if transaction['id'] not in tx_set:
                            asset_info['txs'].append(transaction['id'])
                        asset_dict[tx_output['asset_id']] = asset_info
                    else:
                        continue

        for asset in asset_dict:
            asset_dict[asset].update({'block_hash': block['hash'], 'block_height': block['height']})
        self.save_asset_info(asset_dict)

    def rollback_asset_info(self, block):
        asset_dict = {}
        for transaction in block['transactions']:
            self.logger.debug(
                "begin to deal with tx: %s\naddress_dict:\n%s" % (str(transaction['id']), str(asset_dict)))
            if transaction['status_fail']:
                continue

            for tx_input in transaction['input']:
                if tx_input.get('asset_id').lower() == self.btm_id or \
                        self.mongo_cli.get_one(flags.FLAGS.asset_info,
                                               {'asset_id': tx_input['asset_id'], 'block_hash': block['hash']}) is None:
                    continue
                if tx_input['type'] == 'issue':
                    asset_info = asset_dict.get(tx_input['asset_id'], None) or self.mongo_cli.get_one(
                        flags.FLAGS.address_info, {'asset_id': tx_input['asset_id']})
                    asset_info['txs'] = {}
                elif tx_input['type'] == 'spend':
                    asset_info = asset_dict.get(tx_input['asset_id'], None) or self.mongo_cli.get_one(
                        flags.FLAGS.asset_info, {'asset_id': tx_input['asset_id']})
                    if 'address' not in tx_input:
                        continue

                    if tx_input['address'] not in asset_info['balances']:
                        asset_info['balances'][tx_input['address']] = 0
                    asset_info['balances'][tx_input['address']] += tx_input['amount']
                    tx_set = set(asset_info['txs'])
                    if transaction['id'] in tx_set:
                        asset_info['txs'].remove(transaction['id'])
                    asset_dict[tx_input['asset_id']] = asset_info

                else:
                    continue
                self.logger.debug("address_dict after dealing TI %s:\n%s" % (str(tx_input), str(asset_dict)))
            for tx_output in transaction['outputs']:
                if tx_output.get('asset_id').lower() == self.btm_id or \
                        self.mongo_cli.get_one(flags.FLAGS.asset_info,
                                               {'asset_id': tx_output['asset_id'], 'block_hash': block['hash']}) is None:
                    continue
                if tx_output['type'] == 'control':
                    asset_info = asset_dict.get(tx_output['asset_id'], None) or self.mongo_cli.get_one(
                        flags.FLAGS.asset_info, {'asset_id': tx_output['asset_id']})
                    if 'address' not in tx_output:
                        continue

                    asset_info['balances'][tx_output['address']] -= tx_output['amount']
                    tx_set = set(asset_info['txs'])
                    if transaction['id'] in tx_set:
                        asset_info['txs'].remove(transaction['id'])
                    asset_dict[tx_output['asset_id']] = asset_info

                elif tx_output['type'] == 'retire':
                    asset_info = asset_dict.get(tx_output['asset_id'], None) or self.mongo_cli.get_one(
                        flags.FLAGS.asset_info, {'asset_id': tx_output['asset_id']})
                    asset_info['retire'] -= tx_output['amount']
                    tx_set = set(asset_info['txs'])
                    if transaction['id'] in tx_set:
                        asset_info['txs'].remove(transaction['id'])
                    asset_dict[tx_output['asset_id']] = asset_info
                else:
                    continue
                self.logger.debug("address_dict after dealing TO %s:\n%s" % (str(tx_output), str(asset_dict)))

        self.set_asset_mark(asset_dict)
        self.logger.debug('set asset mark successful: \n%s' % str(asset_dict))
        self.save_asset_info(asset_dict)

    def set_asset_mark(self, asset_dict):
        for key in asset_dict:
            info = asset_dict[key]
            if len(info['txs']) == 0:
                continue
            latest_tx = self.get_one(flags.FLAGS.transaction_info, {'id': info['txs'][-1]})
            info.update({'block_hash': latest_tx['block_hash'], 'block_height': latest_tx['block_height']})

    def remove_highest_block(self, block):
        current_block_hash = block['hash']
        try:
            self.rollback_asset_info(block)
            self.logger.info("remove asset info of block %s | %s: ok" % (str(current_block_hash), str(block['height'])))
            self.rollback_address_info(block)
            self.logger.info("remove address info of block %s | %s: ok" % (str(current_block_hash), str(block['height'])))
            self.mongo_cli.delete_many(flags.FLAGS.transaction_info, {'block_hash': current_block_hash})
            self.logger.info("remove transaction info of block %s | %s: ok" % (str(current_block_hash), str(block['height'])))
            self.mongo_cli.delete_one(flags.FLAGS.block_info, {'hash': current_block_hash})
            self.logger.info("remove block info of block %s | %s: ok" % (str(current_block_hash), str(block['height'])))

        except Exception as e:
            self.logger.error("remove highest block Error: %s\n%s" % (str(e), str(block)))
            raise  Exception

    def rollback_address_info(self, block):
        address_dict = {}
        try:
            for transaction in block['transactions']:
                self.logger.debug("begin to deal with tx: %s\naddress_dict:\n%s" % (str(transaction['id']), str(address_dict)))
                for tx_input in transaction['inputs']:
                    if tx_input['type'] != 'spend' or tx_input.get('asset_id').lower() != self.btm_id:
                        continue

                    address = tx_input.get('address')
                    if not address or self.mongo_cli.get_one(
                            flags.FLAGS.address_info, {'address': address, 'block_hash': block['hash']}) is None:
                        continue

                    address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                             {'address': address})

                    address_info['balance'] += tx_input['amount']
                    address_info['sent'] -= tx_input['amount']
                    if transaction['id'] in address_info['txs']:
                        address_info['txs'].remove(transaction['id'])
                    address_dict[address] = address_info
                    self.logger.debug("address_dict after dealing TI %s:\n%s" % (str(tx_input), str(address_dict)))

                for tx_output in transaction['outputs']:
                    if tx_output['type'] != 'control' or tx_output.get('asset_id').lower() != self.btm_id:
                        continue

                    address = tx_output.get('address')
                    if not address or self.mongo_cli.get_one(
                            flags.FLAGS.address_info, {'address': address, 'block_hash': block['hash']}) is None:
                        continue

                    address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                             {'address': address})
                    address_info['balance'] -= tx_output['amount']
                    address_info['recv'] -= tx_output['amount']
                    if transaction['id'] in address_info['txs']:
                        address_info['txs'].remove(transaction['id'])
                    address_dict[address] = address_info
                    self.logger.debug("address_dict after dealing TO %s:\n%s" % (str(tx_output), str(address_dict)))
        except Exception as e:
            self.logger.error("remove highest block Error: %s\n%s\ndealing tx\n: %s"
                              % (str(e), str(block), str(transaction)))
            raise Exception

        self.set_address_mark(address_dict)
        self.logger.debug('set address mark successful: \n%s' % str(address_dict))
        self.save_address_info(address_dict)

    def set_address_mark(self, address_dict):
        for key in address_dict:
            info = address_dict[key]
            if len(info['txs']) == 0:
                continue
            latest_tx = self.get_one(flags.FLAGS.transaction_info, {'id': info['txs'][-1]})
            info.update({'block_hash': latest_tx['block_hash'], 'block_height': latest_tx['block_height']})

    def save_address_info(self, address_dict):
        for key in address_dict:
            info = address_dict[key]
            if len(info['txs']) == 0:
                self.mongo_cli.delete_one(flags.FLAGS.address_info, {'address': info['address']})
                continue

            self.mongo_cli.update_one(flags.FLAGS.address_info, {'address': info['address']}, {'$set': info}, True)

    def save_asset_info(self, asset_dict):
        for key in asset_dict:
            info = asset_dict[key]
            if len(info['txs']) == 0:
                self.mongo_cli.delete_one(flags.FLAGS.asset_info, {'asset_id': info['asset_id']})
                continue

            balances = asset_dict[key]['balances']
            for address in balances:
                if balances[address] == 0:
                    balances.pop(address)

            self.mongo_cli.update_one(flags.FLAGS.asset_info, {'asset_id': info['asset_id']}, {'$set': info}, True)

    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})

    def remove_future_block(self):
        future_height = self.get_height()+1
        future_block = self.get_block_by_height(future_height)
        if future_block is not None:
            self.remove_highest_block(future_block)
