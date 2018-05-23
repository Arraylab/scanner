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
        self.mongo_cli.insert(flags.FLAGS.block_info, block)
        self.insert_transactions(block)
        self.index_address(block)
        self.update_asset_status(block)
        self.set_height(block['height'])

    def insert_transactions(self, block):
        for transaction in block['transactions']:
            transaction.update({'block_height': block['height'], 'block_hash': block['hash']})
        self.mongo_cli.insert_many(flags.FLAGS.transaction_info, block['transactions'])

    @staticmethod
    def default_address_info(address):
        address_info = {
            'address': address,
            'balance': 0,
            'recv': 0,
            'sent': 0,
            'txs': [],
            'asset_balances': {}
        }
        return address_info

    def index_address(self, block):
        address_dict = {}
        for transaction in block['transactions']:
            for tx_input in transaction['inputs']:
                address = tx_input.get('address', None)
                if tx_input['type'] != 'spend' \
                        or (transaction['status_fail'] and tx_input.get('asset_id').lower() != self.btm_id)\
                        or address is None:
                    continue

                address_info = address_dict.get(address, None) \
                               or self.mongo_cli.get_one(flags.FLAGS.address_info, {'address': address}) \
                               or self.default_address_info(address)

                asset_id = tx_input.get('asset_id').lower()
                if asset_id == self.btm_id:
                    address_info['balance'] -= tx_input['amount']
                    address_info['sent'] += tx_input['amount']
                else:
                    asset_balance = address_info.get('asset_balances').\
                        setdefault(asset_id, {'balance': 0, 'sent': 0, 'recv': 0})
                    asset_balance['balance'] -= tx_input['amount']
                    asset_balance['sent'] += tx_input['amount']

                if transaction['id'] not in address_info['txs']:
                    address_info['txs'].append(transaction['id'])

                address_dict[address] = address_info

            for tx_output in transaction['outputs']:
                address = tx_output.get('address', None)
                if tx_output.get('type') != 'control' \
                        or (transaction['status_fail'] and tx_output.get('asset_id').lower() != self.btm_id)\
                        or address is None:
                    continue

                address_info = address_dict.get(address, None) \
                               or self.mongo_cli.get_one(flags.FLAGS.address_info, {'address': address}) \
                               or self.default_address_info(address)

                asset_id = tx_output.get('asset_id').lower()
                if asset_id == self.btm_id:
                    address_info['balance'] += tx_output['amount']
                    address_info['recv'] += tx_output['amount']
                else:
                    asset_balance = address_info.get('asset_balances').\
                        setdefault(asset_id, {'balance': 0, 'sent': 0, 'recv': 0})
                    asset_balance['balance'] += tx_output['amount']
                    asset_balance['recv'] += tx_output['amount']

                if transaction['id'] not in address_info['txs']:
                    address_info['txs'].append(transaction['id'])

                address_dict[address] = address_info

        for address in address_dict:
            address_dict[address].update({'block_hash': block['hash'], 'block_height': block['height']})
        self.save_address_info(address_dict)

    @staticmethod
    def default_asset_info(asset_id):
        asset_info = {
            'txs': [],
            'balances': {},
            'asset_id': asset_id,
            'retire': 0,
            'asset_definition': {},
            'amount': 0,
            'issue_by': '',
        }
        return asset_info

    def update_asset_status(self, block):
        asset_dict = {}
        for transaction in block['transactions']:
            if transaction['status_fail']:
                continue

            for tx_input in transaction['inputs']:
                asset_id = tx_input.get('asset_id').lower()
                tx_input_type = tx_input.get('type').lower()
                if asset_id == self.btm_id or tx_input_type == 'coinbase':
                    continue

                asset_info = asset_dict.get(tx_input['asset_id'], None) \
                             or self.mongo_cli.get_one(flags.FLAGS.asset_info, {'asset_id': tx_input['asset_id']}) \
                             or self.default_asset_info(asset_id)

                if tx_input_type == 'issue':
                    asset_info.update({
                        'asset_definition': tx_input['asset_definition'],
                        'amount': tx_input['amount'],
                        'issue_by': transaction['id'],
                    })

                elif tx_input_type == 'spend':
                    address = tx_input.get('address', None)
                    if address is None:
                        break
                    if address not in asset_info['balances']:
                        asset_info['balances'][address] = 0
                    asset_info['balances'][address] -= tx_input['amount']
                else:
                    continue

                if transaction['id'] not in asset_info['txs']:
                    asset_info['txs'].append(transaction['id'])
                asset_dict[asset_id] = asset_info

            for tx_output in transaction['outputs']:
                asset_id = tx_output.get('asset_id').lower()
                if asset_id == self.btm_id:
                    continue
                asset_info = asset_dict.get(tx_output['asset_id'], None) \
                             or self.mongo_cli.get_one(flags.FLAGS.asset_info, {'asset_id': tx_output['asset_id']}) \
                             or self.default_asset_info(asset_id)

                if tx_output['type'] == 'control':
                    address = tx_output.get('address', None)
                    if address is None:
                        break
                    if address not in asset_info['balances']:
                        asset_info['balances'][address] = 0
                    asset_info['balances'][address] += tx_output['amount']
                elif tx_output['type'] == 'retire':
                    asset_info['retire'] += tx_output['amount']
                else:
                    continue

                if transaction['id'] not in asset_info['txs']:
                    asset_info['txs'].append(transaction['id'])
                asset_dict[asset_id] = asset_info

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

            for tx_input in transaction['inputs']:
                asset_id = tx_input.get('asset_id').lower()
                tx_input_type = tx_input.get('type').lower()
                if asset_id == self.btm_id or tx_input_type == 'coinbase':
                    continue

                asset_info = asset_dict.get(tx_input['asset_id'], None) \
                             or self.mongo_cli.get_one(flags.FLAGS.asset_info, {'asset_id': asset_id, 'block_hash': block['hash']})
                if asset_info is None:
                    continue

                if tx_input_type == 'issue':
                    asset_info['txs'] = {}
                elif tx_input_type == 'spend':
                    address = tx_input.get('address', None)
                    if address is None:
                        break
                    if address not in asset_info['balances']:
                        asset_info['balances'][address] = 0
                    asset_info['balances'][address] += tx_input['amount']
                else:
                    continue

                if transaction['id'] in asset_info['txs']:
                    asset_info['txs'].remove(transaction['id'])
                asset_dict[tx_input['asset_id']] = asset_info
                self.logger.debug("address_dict after dealing TI %s:\n%s" % (str(tx_input), str(asset_dict)))

            for tx_output in transaction['outputs']:
                asset_id = tx_output.get('asset_id').lower()
                if asset_id == self.btm_id:
                    continue
                asset_info = asset_dict.get(tx_output['asset_id'], None) \
                             or self.mongo_cli.get_one(flags.FLAGS.asset_info, {'asset_id': asset_id, 'block_hash': block['hash']})
                if asset_info is None:
                    continue

                if tx_output['type'] == 'control':
                    address = tx_output.get('address', None)
                    if address is None:
                        break
                    asset_info['balances'][address] -= tx_output['amount']
                elif tx_output['type'] == 'retire':
                    asset_info['retire'] -= tx_output['amount']
                else:
                    continue

                if transaction['id'] in asset_info['txs']:
                    asset_info['txs'].remove(transaction['id'])
                asset_dict[tx_output['asset_id']] = asset_info

                self.logger.debug("address_dict after dealing TO %s:\n%s" % (str(tx_output), str(asset_dict)))

        self.set_asset_mark(asset_dict)
        self.logger.debug('set asset mark successful: \n%s' % str(asset_dict))
        self.save_asset_info(asset_dict)

    def set_asset_mark(self, asset_dict):
        for asset in asset_dict:
            info = asset_dict[asset]
            if len(info['txs']) == 0:
                continue
            latest_tx = self.mongo_cli.get_one(flags.FLAGS.transaction_info, {'id': info['txs'][-1]})
            info.update({'block_hash': latest_tx['block_hash'], 'block_height': latest_tx['block_height']})

    def remove_highest_block(self, block):
        if block['height'] in [538, 502, 473, 1]:
            raise Exception
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
            raise Exception

    def rollback_address_info(self, block):
        address_dict = {}
        try:
            for transaction in block['transactions']:
                self.logger.debug("begin to deal with tx: %s\naddress_dict:\n%s" % (str(transaction['id']), str(address_dict)))
                for tx_input in transaction['inputs']:
                    address = tx_input.get('address', None)
                    if tx_input['type'] != 'spend' \
                            or (transaction['status_fail'] and tx_input.get('asset_id').lower() != self.btm_id) \
                            or address is None:
                        continue

                    address_info = address_dict.get(address, None) \
                                   or self.mongo_cli.get_one(flags.FLAGS.address_info, {'address': address, 'block_hash': block['hash']})
                    if address_info is None:
                        continue

                    asset_id = tx_input.get('asset_id').lower()
                    if asset_id == self.btm_id:
                        address_info['balance'] += tx_input['amount']
                        address_info['sent'] -= tx_input['amount']
                    else:
                        asset_balance = address_info.get('asset_balances').\
                            setdefault(asset_id, {'balance': 0, 'sent': 0, 'recv': 0})
                        asset_balance['balance'] += tx_input['amount']
                        asset_balance['sent'] -= tx_input['amount']

                    if transaction['id'] in address_info['txs']:
                        address_info['txs'].remove(transaction['id'])
                    address_dict[address] = address_info
                    self.logger.debug("address_dict after dealing TI %s:\n%s" % (str(tx_input), str(address_dict)))

                for tx_output in transaction['outputs']:
                    address = tx_output.get('address', None)
                    if tx_output['type'] != 'control' \
                            or (transaction['status_fail'] and tx_output.get('asset_id').lower() != self.btm_id) \
                            or address is None:
                        continue

                    address_info = address_dict.get(address, None) \
                                   or self.mongo_cli.get_one(flags.FLAGS.address_info, {'address': address, 'block_hash': block['hash']})
                    if address_info is None:
                        continue

                    asset_id = tx_output.get('asset_id').lower()
                    if asset_id == self.btm_id:
                        address_info['balance'] -= tx_output['amount']
                        address_info['recv'] -= tx_output['amount']
                    else:
                        asset_balance = address_info.get('asset_balances').\
                            setdefault(asset_id, {'balance': 0, 'sent': 0, 'recv': 0})
                        asset_balance['balance'] -= tx_output['amount']
                        asset_balance['recv'] -= tx_output['amount']

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
        for address in address_dict:
            info = address_dict[address]
            if len(info['txs']) == 0:
                continue
            latest_tx = self.mongo_cli.get_one(flags.FLAGS.transaction_info, {'id': info['txs'][-1]})
            info.update({'block_hash': latest_tx['block_hash'], 'block_height': latest_tx['block_height']})

    def save_address_info(self, address_dict):
        for address in address_dict:
            info = address_dict[address]
            balances = info['asset_balances']
            if len(info['txs']) == 0:
                self.mongo_cli.delete_one(flags.FLAGS.address_info, {'address': info['address']})
                continue

            info['asset_balances'] = {asset_id: balance for asset_id, balance in balances.items()
                                      if cmp(balance, {'balance': 0, 'sent': 0, 'recv': 0}) != 0}

            self.mongo_cli.update_one(flags.FLAGS.address_info, {'address': info['address']}, {'$set': info}, True)

    def save_asset_info(self, asset_dict):
        for asset_id in asset_dict:
            info = asset_dict[asset_id]
            balances = info['balances']
            if len(info['txs']) == 0:
                self.mongo_cli.delete_one(flags.FLAGS.asset_info, {'asset_id': info['asset_id']})
                continue

            info['balances'] = {address: balance for address, balance in balances.items() if balance != 0}

            self.mongo_cli.update_one(flags.FLAGS.asset_info, {'asset_id': info['asset_id']}, {'$set': info}, True)

    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})

    def remove_future_block(self):
        future_height = self.get_height()+1
        future_block = self.get_block_by_height(future_height)
        if future_block is not None:
            self.remove_highest_block(future_block)
