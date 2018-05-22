import json

import requests

from tools import flags


# fetch info from bytomd
class Fetcher:
    def __init__(self):
        self.url_base = flags.FLAGS.bytomd_rpc

    def request_block(self, block_height):
        params = json.dumps({flags.FLAGS.get_block_height_arg: block_height})
        url = '/'.join([self.url_base, flags.FLAGS.get_block])

        response = requests.post(url, params).json()
        if response['status'] == 'fail':
            raise Exception('get block failed: %s', response['msg'])

        return response['data']

    def request_chain_height(self):
        url = '/'.join([self.url_base, flags.FLAGS.get_block_count])
        response = requests.post(url).json()
        if response['status'] == 'fail':
            raise Exception('get chain height failed: %s', response['msg'])

        return response['data'][flags.FLAGS.block_count]

    def request_hash_rate(self, block_hash):
        params = json.dumps({'block_hash': block_hash})
        url = '/'.join([self.url_base, flags.FLAGS.get_hash_rate])
        response = requests.post(url, params).json()
        if response['status'] == 'fail':
            raise Exception('get hash rate failed: %s', response['msg'])
        return response['data']['hash_rate']
