#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os import  sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import unittest
import requests
import random
import config
from base_mod import  BitcoinTestCase
from urls import get_api_url

    
class StatTest(BitcoinTestCase):
    """
    bitcoin tests case
    """

    def test_market_info(self):
        '''
                获取价格和24hr统计信息
        :return: json
        '''
        url = get_api_url('market_info') 
        res = requests.get(url).json()
        self.assert_request_success(res)
        
                   
    def test_stat_info(self):
        '''
                    获取区块链统计信息
        :return: json
        '''
        url = get_api_url('stat_info') 
        #blockchain stat
        res = requests.get(url+'/blockchain').json()
        self.assert_request_success(res)

        #tx stat
        res = requests.get(url+'/tx').json()
        self.assert_request_success(res)
        
        #block stat
        res = requests.get(url+'/block').json()
        self.assert_request_success(res)
        
        #address stat
        res = requests.get(url+'/address').json()
        self.assert_request_success(res)    

            
    
    
    
    
 