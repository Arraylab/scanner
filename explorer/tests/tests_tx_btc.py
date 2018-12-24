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

    
class TxTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_tx_info(self):
        '''
                    获取交易信息
        :return: json
        '''
        url = get_api_url('tx_info')   
        
        for tx_hash in config.TX_HASHS:
            #test tx in short
            res = requests.get(url+'/%s?detail=0&chain=bitcoin' % tx_hash).json()
            self.assert_request_success(res)
            #test tx in detail
            res = requests.get(url+'/%s?detail=1&chain=bitcoin' % tx_hash).json()
            self.assert_request_success(res)
            self.assert_in(res, 'inputs', 'script')
            self.assert_in(res, 'outputs', 'script')

    
    
 