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


class AddressTest(EthereumTestCase):
    """
    ethereum tests case
    """

    def test_address_info(self):
        '''
        获取地址信息
        :return: json
        '''
        url = get_api_url('address_info')
        params = {
            'chain' : "ethereum"
        }
        ''' 1 normal account '''
        # normal info
        addr = config.ETHERUM_ADDRESS[0]
        
        params['filter'] = 'tx'
        res = requests.get(url+'/%s' % addr, params = params).json()
        self.assert_request_success(res)
        self.assertEqual(res['data']['contract_flag'], False)
        self.assertEqual(res['data']['miner_flag'], False)      
        txs = res['data']['tx']    
        self.assertEqual(len(txs), 10)
        self.assertEqual(res['data']['pages'], 81)
        # miner info
        addr = config.ETHERUM_ADDRESS[1]
        
        params['filter'] = 'mine'
        res = requests.get(url+'/%s' % addr, params = params).json()
        self.assert_request_success(res) 
        self.assertEqual(res['data']['contract_flag'], False)
        self.assertEqual(res['data']['miner_flag'], True)        
        mine = res['data']['mine']    
        self.assertEqual(len(mine), 10)
        self.assertEqual(res['data']['pages'], 47)

        params['filter'] = 'uncles'
        res = requests.get(url+'/%s' % addr, params = params).json()
        self.assert_request_success(res) 
        self.assertEqual(res['data']['contract_flag'], False)  
        self.assertEqual(res['data']['miner_flag'], True)  
        uncles = res['data']['uncles']    
        self.assertEqual(len(uncles), 10)
        self.assertEqual(res['data']['pages'], 6)
           
   
        ''' 2 contract account '''
        # contract account
        # DGD
        addr = "0xe0b7927c4af23765cb51314a0e0521a9645f0e2a"
        params['filter'] = 'tx'
        res = requests.get(url+'/%s' % addr, params = params).json()
        self.assert_request_success(res)
        self.assertEqual(res['data']['miner_flag'], False) 
        self.assertEqual(res['data']['contract_flag'], True)
        self.assertIn("abi", res['data'])
        self.assertIn("source_code", res['data'])

















