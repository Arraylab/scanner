#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os import  sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import requests
import json
import random
import btc_config as config
from base_mod import  BitcoinTestCase
from urls import get_api_url
from blockmeta import cache_module
from blockmeta import flags
from settings import HOST
FLAGS = flags.FLAGS
import time

class SearchTest(BitcoinTestCase):
    """
    etheruem tests case
    """
    def setUp(self):
        pass
    
    def test_search_block(self):
        # multi is False
        url = get_api_url('search_info')
        params = {
            'chain' : "bitcoin",
            'q' : '',
        }
        headers = {'content-type': 'application/json'}
        
        for block_height in config.BLOCK_IDS:
            params['q'] = block_height
            res = requests.post(url, data=json.dumps(params), headers=headers).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求成功')


        for block_hash in config.BLOCK_HASHS:
            params['q'] = block_hash
            res = requests.post(url, data=json.dumps(params), headers=headers).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求成功')
            
    
    def test_search_tx(self):
        url = get_api_url('search_info')
        params = {
            'chain' : "bitcoin",
            'q' : '',
        }
        headers = {'content-type': 'application/json'}
        for tx_hash in config.TX_HASHS:
            params['q'] = tx_hash
            res = requests.post(url, data=json.dumps(params), headers=headers).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')
            


    def test_search_address(self):
        url = get_api_url('search_info')
        params = {
            'chain' : "bitcoin",
            'q' : '',
        }
        headers = {'content-type': 'application/json'}
        for addr in config.ADDRESSES:
            params['q'] = addr
            res = requests.post(url, data=json.dumps(params), headers=headers).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求失败')

    
    def test_search_pattern(self):
        
        url = get_api_url('search_info')
        params = {
            'chain' : "bitcoin",
            'q' : '',
        }   
        headers = {'content-type': 'application/json'}
        for pattern in config.SEARCH_PATTERN:
            params['q'] = pattern
            res = requests.post(url, data=json.dumps(params), headers=headers).json()
            self.assertEqual(res['code'], '302')
            self.assertEqual(res['status'], 'success', msg=u'请求成功')
            
            
    def tearDown(self):
        pass