#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os import  sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import requests
import random
import btc_config as config
from base_mod import  BitcoinTestCase
from urls import get_api_url

    
class BlockTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_block_info(self):
        '''
                   获取区块信息
        :return: json
        '''
        url = get_api_url('block_info')        
        block_height = 330000 
        
        
        for i in range(3):
            #test block height
            chain = '?chain=bitcoin'
            page = '&page=%d' % i if i else ''
            res = requests.get(url+'/%d' % block_height+chain+page).json()
            self.assert_request_success(res)
            self.assert_equal(res, 'height', block_height) 
        
            #test block hash 
            for block_hash in config.BTC_BLOCK_HASHS:        
                res = requests.get(url+'/%s' % block_hash +chain+page).json()
                self.assert_request_success(res)
                self.assert_equal(res, 'hash', block_hash) 
        
        #test block list
        res = requests.get(url+'s?chain=bitcoin').json()
        self.assert_request_success(res)
        self.assert_len(res['data'], 6) 
    
    
        res = requests.get(url+'s?start=0&offset=30&chain=bitcoin').json()
        self.assert_request_success(res)
        self.assert_len(res['data'], 30) 
