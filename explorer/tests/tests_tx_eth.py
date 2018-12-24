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


class TxTest(EthereumTestCase):
    """
    ethereum tests case
    """

    def test_tx_info(self):
        '''
                    获取交易信息
        :return: json
        '''
        url = get_api_url('tx_info')

        params = {
            "chain":"ethereum"
        }

        # normal test
        for tx_hash in config.ETH_TX_HASHS:
            #test tx
            res = requests.get(url+'/%s?detail=0' % tx_hash, params = params).json()
            self.assert_request_success(res)
            #test tx in detail
            res = requests.get(url+'/%s?detail=1' % tx_hash, params = params).json()
            self.assert_request_success(res)
        
	# tx trigger token transfer
        res = requests.get(url+'/%s?detail=0' % config.ETH_TX_TRI_TOKEN, params = params).json()
        self.assert_request_success(res)
        tx = res['data']['tx']
        self.assertEqual(tx['hash'], config.ETH_TX_TRI_TOKEN)
        token_txs = res['data']['token_txs']
	
	'''
        DCS_token_txs = token_txs["DCS"]
        for tx in DCS_token_txs:
            self.assertEqual(tx['transactionHash'][2:], config.ETH_TX_TRI_TOKEN)
        
        # tx triggle internal transfer
        res = requests.get(url+'/%s?detail=0' % config.ETH_TX_TRI_INTERNAL, params = params).json()
        self.assert_request_success(res)
        tx = res['data']['tx']
        self.assertEqual(tx['hash'], config.ETH_TX_TRI_INTERNAL)
        '''
        # tx list without param
        res = requests.get(url+'s', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['txs'], 10)

        # tx list with page param
        for i in range(10, 100):
            res = requests.get(url+'s?page=%d' % i, params = params).json()
            self.assert_request_success(res)
            self.assert_len(res['data']['txs'], 10)
            for _ in range(0, 9):
                tx1 = res['data']['txs'][_]
                tx2 = res['data']['txs'][_+1]
                self.assertGreaterEqual(tx1['timestamp'], tx2['timestamp'])

        # tx list with start offset param
        res = requests.get(url+'s?start=0&offset=30', params = params).json()
        self.assert_request_success(res)
        self.assert_len(res['data']['txs'], 30)




