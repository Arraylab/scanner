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

    
class ArchivesTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_archives_info(self):
        '''
                    获取地址信息
        :return: json
        '''
        url = get_api_url('archives_info')
        
        res = requests.get(url+'/list?start=0&offset=15').json()
        self.assert_request_success(res)
        
        for f in config.ARCHIVES_FILTERS:
            res = requests.get(url+'/list?start=0&offset=15&filter=%s' % f).json()
            self.assert_request_success(res)
            res = requests.get(url+'/list?start=15&offset=30&filter=%s' % f).json()
            self.assert_request_success(res)

        
        url = get_api_url('archives_noted_info')
        for f in config.ARCHIVES_FILTERS:
            res = requests.get(url+'/list_noted?start=0&offset=15&filter=%s' % f).json()
            self.assert_request_success(res)

        
            




        

            
    
    
    
    
 