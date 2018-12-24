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

    
class MinerTest(BitcoinTestCase):
    """
    miner tests case
    """
    
    def test_miner_info(self):
        '''
                   获取区块信息
        :return: json
        '''
        url = get_api_url('miner_info')        
        
        
        for miner in config.MINERS:
            res = requests.get(url+'/%s?chain=bitcoin&page=2' % miner).json()
            self.assert_request_success(res)
        
