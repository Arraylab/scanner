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


    
class ApiTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_api_info(self):
        '''
                     测试对外API信息
        :return: json
        '''
        url = get_api_url('api_info') 
        
        SIMPLE_APIS = ['getdifficulty', 'getblockcount', 'reward', 'chainsize', 'totalbtc', 'interval',
                       'hashrate', 'avgtxnum', 'nextdifficulty', 'lastminer', 'lastblockhash', 'unconfirmedcount',
                       '24hrpoolstat', '24hrblockcount',  'ticker', ]
        
        #simple API
        for api in SIMPLE_APIS:
            res = requests.get(url+'/chain/%s' % api).json()
            self.assert_request_success(res) 
        
        #tx api
        txid = "34668ec700f9ed6037d473830c0d47548bf8462c1e83bc0a2380dda74aded84e"
        
        self.__request_assert(url+'/tx/info/%s' % txid)
        self.__request_assert(url+'/tx/raw/%s' % txid)

        
        txids = ','.join(id for id in config.TX_HASHS)
            
        self.__request_assert(url+'/tx/info/%s' % txids)
        self.__request_assert(url+'/tx/raw/%s' % txids)

        #block api
        h1, h2, h3 = 310021, 232132, 23
        bhash = "00000000000000000612c5c994f64af6722fa20f209a98e367b58a141615cc0d"
        bhashs = ','.join(id for id in config.BLOCK_HASHS)
        self.__request_assert(url+'/block/info/%d' % h1)
        self.__request_assert(url+'/block/info/%s' % bhash)
        self.__request_assert(url+'/block/info/%s' % bhashs)
        self.__request_assert(url+'/block/info/%d,%d,%d' % (h1, h2, h3))
        self.__request_assert(url+'/block/info/first,last')

        self.__request_assert(url+'/block/raw/%d' % h1)
        self.__request_assert(url+'/block/raw/%s' % bhash)
        self.__request_assert(url+'/block/raw/%s' % bhashs)
        self.__request_assert(url+'/block/raw/%d,%d,%d' % (h1, h2, h3))
        self.__request_assert(url+'/block/raw/first,last')
        
        self.__request_assert(url+'/block/tx/%d' % h1)
        self.__request_assert(url+'/block/tx/%s' % bhash)
        self.__request_assert(url+'/block/tx/%s' % bhashs)
        self.__request_assert(url+'/block/tx/%d,%d,%d' % (h1, h2, h3))
        self.__request_assert(url+'/block/tx/first,last')
        
        
        #address api
        addr = "1EkRKXzUhkoz1LvYS4MU1NJzMQPuWi7hAZ"
        self.__request_assert(url+'/address/info/%s' % addr)
        self.__request_assert(url+'/address/unconfirmed/%s' % addr)
        self.__request_assert(url+'/address/unspent/%s' % addr)
        
        addrs = ','.join(addr for addr in config.ADDRESSES)
        self.__request_assert(url+'/address/info/%s' % addr)
        self.__request_assert(url+'/address/unconfirmed/%s' % addr)
        self.__request_assert(url+'/address/unspent/%s' % addr)
        
        #tool api
        dbhash = '90ba214202df2979e3f8866b9a65b7935d2df530'
        self.__request_assert(url+'/tool/hashtoaddress?q=%s' % dbhash)
        self.__request_assert(url+'/tool/hashtoaddress?q=%s&v=0' % dbhash)
        self.__request_assert(url+'/tool/addresstohash?q=%s' % dbhash)


    def __request_assert(self, url):
        res = requests.get(url).json()
        self.assert_request_success(res)

        
        


            
    
    
    
    
 