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


class TokenTest(EthereumTestCase):
    """
    ethereum tests case
    """

    def test_token_info(self):
        '''
        获取地址信息
        :return: json
        '''
        url = get_api_url('token_info')
        params = {
            'chain' : "ethereum"
        }

        # token level
        filters = ['tx', "holder"]
        for f in filters:
            res = requests.get(url+'/DGD?filter=%s' % f, params = params).json()
            self.assert_request_success(res)
            data = res['data']
            req_content =  data[f]
            self.assertEqual(len(req_content), 10)
           

        # account level
        filters = ['in', "out"]
        addr = "0x6bdf7b73632379960c4dc25f9f6b2c92ecefde4d"
        for f in filters:
            res = requests.get(url+'/DGD?filter=%s&a=%s' % (f, addr), params = params).json()
            self.assert_request_success(res)
            data = res['data']
            self.assertIn(f, res['data'])
            


















