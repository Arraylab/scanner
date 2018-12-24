#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os import  sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import requests
import random
import eth_config as config
from base_mod import  EthereumTestCase
from urls import get_api_url
from blockmeta import cache_module
from blockmeta import flags
from blockmeta import dbproxy
from settings import HOST
FLAGS = flags.FLAGS
import time

class SearchTest(EthereumTestCase):
    """
    etheruem tests case
    """
    def setUp(self):
        pass
    
    def test_search_block(self):
        # multi is False
        url = get_api_url('search_info')
        block_heights = config.BLOCK_IDS
        params = {
            'chain' : "ethereum",
            'q' : '',
        }
        
        for block_height in block_heights:
            params['q'] = block_height
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            
            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum"}).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['number'], block_height)

        for block_hash in config.ETH_BLOCK_HASHS:
            params['q'] = block_hash
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            
            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum"}).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['hash'], block_hash)

        for block_hash in config.ETH_BLOCK_HASHS:
            params['q'] = block_hash[2:]
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            
            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum"}).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['hash'], block_hash)
        
        # uncle
        for block_hash in config.ETH_UNCLES:
            params['q'] = block_hash
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            
            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum"}).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['hash'], block_hash)

        for token in ["DGD", "DCS"]:
            params['q'] = token
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            
            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum"}).json()
            self.assert_request_success(res)
    
    
    def test_search_tx(self):
        url = get_api_url('search_info')
        params = {
            'chain' : "ethereum",
            'q' : '',
        }
        for tx_hash in config.ETH_TX_HASHS:
            params['q'] = tx_hash
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            #test tx in detail
            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum", "detail":0}).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['tx']['hash'], tx_hash)


    def test_search_address(self):
        url = get_api_url('search_info')
        params = {
            'chain' : "ethereum",
            'q' : '',
        }
        for addr in config.ETHERUM_ADDRESS[1:]:
            params['q'] = addr
            res = requests.post(url, params = params).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')

            redirect_url = HOST + "/api/" + res['data']["type"] + "/" + res['data']["value"]
            res = requests.get(redirect_url, params = {"chain":"ethereum"}).json()
            self.assert_request_success(res)
            self.assertEqual(res['data']['address'], addr)
    
    def tearDown(self):
        pass