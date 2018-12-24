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

    
class AddressTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_address_info(self):
        '''
                    获取地址信息
        :return: json
        '''
        url = get_api_url('address_info')
        
        for addr in config.ADDRESSES:
            #single url
            res = requests.get(url+'/%s?chain=bitcoin' % addr).json()
            self.assert_request_success(res)
        
            for f in config.FILTERS:
                page = '?page=2'
                filter = '&filter=%s&chain=bitcoin' % f
                res = requests.get(url+'/%s' % addr + page + filter).json()
                self.assert_request_success(res)


            




        

            
    
    
    
    
 