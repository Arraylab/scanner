from collector.db.mongodriver import MongodbClient
from tools import flags


class DbProxy:
    btm_id = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

    def __init__(self):
        self.url_base = flags.FLAGS.bytomd_rpc

        self.mongo_cli = MongodbClient(host=flags.FLAGS.mongo_bytom_host, port=flags.FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(flags.FLAGS.mongo_bytom)

    def get_height(self):
        state = self.mongo_cli.get(flags.FLAGS.db_status)
        return None if state is None else state[flags.FLAGS.block_height]

    def set_height(self, height):
        self.mongo_cli.update_one(flags.FLAGS.db_status, {}, {'$set': {flags.FLAGS.block_height: height}}, True)

    def save_block(self, block):
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
                        'txs': []
                    }
                address_info['balance'] += tx_output['amount']
                address_info['recv'] += tx_output['amount']
                txs_set = set(address_info['txs'])
                if transaction['id'] not in txs_set:
                    address_info['txs'].append(transaction['id'])
                address_dict[address] = address_info

        self.save_address_info(address_dict, block['hash'])

    # ignore type destory
    # ignore rollback
    def update_asset_status(self, block):
        asset_dict = {}
        for transaction in block['transactions']:
            for tx_input in transaction['inputs']:
                if tx_input.get('asset_id').lower() != self.btm_id:
                    if tx_input['type'] == 'issue':
                        asset_dict[tx_input['asset_id']] = {
                            'asset_id': tx_input['asset_id'],
                            'amount': tx_input['amount'],
                            'issue_by': transaction['id'],
                            'txs': [transaction['id']],
                            'balances': {}
                        }
                    elif tx_input['type'] == 'spend':
                        asset_info = asset_dict.get(tx_input['asset_id'], None) or self.mongo_cli.get_one(
                            flags.FLAGS.asset_info, {'asset': tx_input['asset_id']})
                        if 'address' not in tx_input:
                            continue

                        asset_info['balances'][tx_input['address']] -= tx_input['amount']
                        if asset_dict['balances'][tx_input['address']] == 0:
                            asset_dict['balances'].pop(tx_input['address'])

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
                            flags.FLAGS.asset_info, {'asset': tx_output['asset_id']})
                        if 'address' not in tx_output:
                            continue

                        if tx_output['address'] not in asset_info['balances']:
                            asset_info['balances'][tx_output['address']] = 0
                        asset_info['balances'][tx_output['address']] += tx_output['amount']
                        tx_set = set(asset_info['txs'])
                        if transaction['id'] not in tx_set:
                            asset_info['txs'].append(transaction['id'])
                        asset_dict[tx_output['asset_id']] = asset_info
                    else:
                        continue

        self.save_asset_info(asset_dict, block['hash'])

    def remove_highest_block(self, block):
        current_block_hash = block['hash']
        self.rollback_address_info(block)
        self.mongo_cli.delete_many(flags.FLAGS.transaction_info, {'block_hash': current_block_hash})
        self.mongo_cli.delete_one(flags.FLAGS.block_info, {'hash': current_block_hash})

    def rollback_address_info(self, block):
        address_dict = {}
        for transaction in block['transactions']:
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
                address_info['txs'].remove(transaction['id'])
                address_dict[address] = address_info

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

        self.save_address_info(address_dict, block['previous_block_hash'])

    def save_address_info(self, address_dict, block_hash):
        for key in address_dict:
            info = address_dict[key]
            if len(info['txs']) == 0:
                self.mongo_cli.delete_one(flags.FLAGS.address_info, {'address': info['address']})
                continue

            info.update({'block_hash': block_hash})
            self.mongo_cli.update_one(flags.FLAGS.address_info, {'address': info['address']}, {'$set': info}, True)

    # asset_dict[tx_input['asset_id']] = {
    #     'amount': tx_input['amount'],
    #     'issue_by': transaction['id'],
    #     'txs': [transaction['id']],
    #     'balances': {}
    # }
    def save_asset_info(self, asset_dict, block_hash):
        for key in asset_dict:
            info = asset_dict[key]
            if len(info['txs']) == 0:
                self.mongo_cli.delete_one(flags.FLAGS.asset_info, {'asset': info['asset_id']})
                continue

            info.update({'block_hash': block_hash})
            self.mongo_cli.update_one(flags.FLAGS.asset_info, {'asset': info['asset_id']}, {'$set': info}, True)

    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})

    def remove_future_block(self):
        future_height = self.get_height()+1
        future_block = self.get_block_by_height(future_height)
        if future_block is not None:
            self.remove_highest_block(future_block)
