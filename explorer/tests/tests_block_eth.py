#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os import  sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import requests
import random
import eth_config as config
from base_mod import EthereumTestCase
from urls import get_api_url

class BlockTest(EthereumTestCase):
    """
    ethereum tests case
    """

    def test_block_info(self):
        '''
        获取区块信息
        :return: json
        '''
        url = get_api_url('block_info')
        block_heights = config.BLOCK_IDS


        params = {
            'chain' : "ethereum"
        }

        # genesis block and normal block by block number
        for block_height in block_heights:
            res = requests.get(url + "/%s" % block_height, params = params).json()
            self.assert_request_success(res)
            self.assert_equal(res, 'number', block_height)
            self.assertIn("confirmation", res["data"])

        # genesis block and normal block by block hash
        for block_hash in config.ETH_BLOCK_HASHS:
            url2 = url + '/%s' % block_hash
            res = requests.get(url2, params = params).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['hash'], block_hash)

        # test block with page param
        for i in range(1, 5):
            res = requests.get(url+'/0?page=%d' % i, params = params).json()
            self.assert_request_success(res)
            self.assert_len(res['data']['transactions'], 10)

        res = requests.get(url+'/0?page=890', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['transactions'], 3)

        res = requests.get(url+'/0?page=891', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['transactions'], 0)

        # test block list without param
        res = requests.get(url+'s', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['blocks'], 10)

        # test block list with page param
        res = requests.get(url+'s?page=1', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['blocks'], 10)

        # test block list with start offset param
        res = requests.get(url+'s?start=0&offset=30', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['blocks'], 30)
        for _ in range(0, 29):
            blk1 = res['data']['blocks'][_]
            blk2 = res['data']['blocks'][_+1]
            self.assertGreaterEqual(blk1['number'], blk2['number'])

