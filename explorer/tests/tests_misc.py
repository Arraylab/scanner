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

    
class MiscTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_abouts(self):
        '''
                    获取文案信息
        :return: json
        '''
        url = get_api_url('abouts_info')
        res = requests.get(url).json()
        self.assert_request_success(res)
        
    
    def test_search(self):
        '''
                搜索测试
       :return: json
       '''
        url = get_api_url('search_info')        
        for sp in config.SEARCH_PATTERN:
            pay_load = {'q': sp}
            res = requests.post(url, data=pay_load).json()
            self.assert_request_modified(res)
