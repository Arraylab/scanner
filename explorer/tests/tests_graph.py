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

    
class GraphTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_qrcode(self):
        '''
                   测试二维码信息
        :return: json
        '''
        url = get_api_url('qr_info')        
        res = requests.get(url+'?data=1NkAKsHPpT5LAaDPCMoL9hGG2vT9EbeRbB&size=200')
        self.__assert_binary(res)
        
    
    def test_captcha_code(self):
        '''
                    测试验证码
        :return: json
        '''
        url = get_api_url('captcha_info') 
        res = requests.get(url+'?width=10&height=20')
        self.__assert_binary(res)
        
    def test_logo(self):
        '''
                    测试logo
        :return: json
        '''
        url = get_api_url('logo_info') 
        for name in config.LOGOS:
            res = requests.get(url+'?name=%s&width=10&height=20' % name)
            self.__assert_binary(res)       
    
    
    def __assert_binary(self, res):
        content, status_code = res.content, res.status_code
        self.assert_raw_success(status_code, content)
