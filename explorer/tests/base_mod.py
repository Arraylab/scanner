#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import blockmeta
import requests
import base64, hashlib
import hmac
import time
from urls import get_api_url
from settings import HOST, EMAIL, PASSWORD

#from blockmeta.account.auth import int_to_base32_str


class BaseTestCase(unittest.TestCase):
    """
    some init work
    """
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        """
        setup fixtures
        :return:
        """
        self.app = blockmeta.app
        self.host = HOST

        # login and get the token
        url = get_api_url('login')
        res = requests.post(url, data={'email': EMAIL, 'password': PASSWORD})

        assert res.json()['code'] == u'200', u'登录失败'
        assert res.json()['status'] == 'success', u'登录失败'
        self.token = res.cookies.get('token')
        self.key = res.cookies.get('key')
        data = res.json()['data']
        self.user_id = data['user_id']
        self.remote_ip = data['remote_ip']
        self.csrf_token = self._generate_csrf_token()

        self.cookies = {'token': self.token, 'key': self.key}
        self.headers = {'csrf-token': self.csrf_token}


    def tearDown(self):
        """
        tear down the fixtures
        :return:
        """
        pass

    def assert_request_success(self, res):
        """
        测试请求是否成功
        :param res:
        :return:
        """
        self.assertEqual(res['code'], '200', msg=u'code != 200')
        self.assertEqual(res['status'], 'success', msg=u'请求失败')

    def auth_post(self, url, data=None, ex_json=True):
        """
        POST need authenticated
        :param url:
        :param data: post data
        :return:
        """
        if ex_json:
            return requests.post(url, data=data, headers=self.headers, cookies=self.cookies).json()
        return requests.post(url, data=data, headers=self.headers, cookies=self.cookies)

    def auth_get(self, url, ex_json=True):
        """
        GET need authenticated
        :param url:
        :return:
        """
        if ex_json:
            return requests.get(url, cookies=self.cookies).json()
        return requests.get(url, cookies=self.cookies)

    def _generate_csrf_token(self):
        key = self.key

        key, times = key.split(':')
        s = 'user_id:' + str(self.user_id) + 'ip:' + self.remote_ip + '.' + key

        for i in range(int(times)):
            s = hmac.new(str(key), str(s), hashlib.md5).hexdigest()

        key = int(key, 16)  # 16进制到10进制
        key = int_to_base32_str(key)  # 转32进制

        s2 = ""
        for i in range(int(times)):
            for k in key:
                x = int(ord(k))
                if x < 97:
                    x += 39
                x -= 87
                s2 += s[x]
        s2 = hmac.new(key, s2, hashlib.md5).hexdigest()
        csrf_token = base64.b64encode(s2+'.'+str(int(time.time())))
        return csrf_token


class BitcoinTestCase(unittest.TestCase):
    """
    some init work
    """
    def __init__(self, *args, **kwargs):
        super(BitcoinTestCase, self).__init__(*args, **kwargs)

    def assert_request_success(self, res, type=dict):
        """
                测试请求是否成功
        :param res:
        :return:
        """

        self.assertEqual(res['code'], '200')
        self.assertEqual(res['status'], 'success', msg=u'请求失败')

    def assert_equal(self, res, v1, v2):
        self.assertEqual(res['data'].get(v1), v2, msg=u'值不相等')

    def assert_len(self, rlist, n):
        self.assertEqual(len(rlist), n, msg=u'长度不对')

    def assert_in(self, res, v1, v2):
        data = res['data'].get(v1)
        if type(data) == list:
            for arg in data:
                self.assertIn(v2, arg)
        else:
            self.assertIn(v2, data)


    def assert_request_modified(self, res, type=dict):
        self.assertEqual(int(res['code']), 302, msg=u'code != 302')
        self.assertEqual(res['status'], 'success', msg=u'请求失败')

EthereumTestCase = BitcoinTestCase


