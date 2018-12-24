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

    
class ChartTest(BitcoinTestCase):
    """
    bitcoin tests case
    """
    
    def test_chart_info(self):
        '''
                    获取图表信息
        :return: json
        '''
        #self.__test_charts()
        #self.__test_chain_chart()
        #self.__test_block_chart()
        #self.__test_address_chart()
        #self.__test_miner_chart()
        self.__test_tx_chart()
    
    def __test_charts(self):

        url = get_api_url('charts_info')
        for chart in config.KNOWN_CHARTS:
            res = requests.get(url+'/%s' % chart).json()
            self.assert_request_success(res)
        
    def __test_chain_chart(self):
        timespan = [1, 2, 6, 12, 24, 100]
        
        url = get_api_url('chain_chart_info')
        for chart in config.CHAIN_CHARTS:
            for ts in timespan:
                res = requests.get(url+'/%s?timespan=%d&linear=0' % (chart, ts)).json()
                self.assert_request_success(res)
                res = requests.get(url+'/%s?timespan=%d&linear=1' % (chart, ts)).json()
                self.assert_request_success(res)

    def __test_block_chart(self):
        timespan = [1, 2, 6, 12, 24, 100]
        
        url = get_api_url('block_chart_info')
        for chart in config.BLOCK_CHARTS:
            for ts in timespan:
                res = requests.get(url+'/%s?timespan=%d&linear=0' % (chart, ts)).json()
                self.assert_request_success(res)
                res = requests.get(url+'/%s?timespan=%d&linear=1' % (chart, ts)).json()
                self.assert_request_success(res)
        
        url = get_api_url('block_index_chart_info')

        timespan = [1, 7, 30]
        for chart in config.BLOCK_INDEX_CHARTS:
            for ts in timespan:
                res = requests.get(url+'/%s?timespan=%d' % (chart, ts)).json()
                self.assert_request_success(res)
       
    def __test_tx_chart(self):
        
        start_point = [0, 10, 20]
        
        url = get_api_url('tx_chart_info')
        for chart in config.TX_CHARTS:
            for s in start_point:
                res = requests.get(url+'?start=%d&offset=%d&type=%s' % (s, s+10, chart)).json()
                self.assert_request_success(res)
        
    
    
    def __test_address_chart(self):
        timespan = [1, 2, 6, 12, 24, 100]
        
        addr = '1HstuMgmBZkLGBTPLH7U6HQjRZDvwc7J2M'
        
        url = get_api_url('address_chart_info')
        for chart in config.ADDRESS_CHARTS:
            for ts in timespan:
                res = requests.get(url+'/%s?q=%s&timespan=%d&linear=0' % (chart, addr, ts)).json()
                self.assert_request_success(res)
                res = requests.get(url+'/%s?q=%s&timespan=%d&linear=1' % (chart, addr, ts)).json()
                self.assert_request_success(res)  
 
         
    def __test_miner_chart(self):
        timespan = [1, 2, 6, 12, 24, 100]
        
        url = get_api_url('miner_chart_info')
        for chart in config.MINERS:
            for ts in timespan:
                res = requests.get(url+'/%s?timespan=%d&linear=0' % (chart, ts)).json()
                self.assert_request_success(res)
                res = requests.get(url+'/%s?timespan=%d&linear=1' % (chart, ts)).json()
                self.assert_request_success(res)
 