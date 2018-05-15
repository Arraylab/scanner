#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g
import json
import time
import re

ERROR_MSG = {
    'zh' :{
        'market_error': '市场数据无法获得',
        'tx_error': '交易信息查询失败',
        'block_error': '区块信息查询失败',
        'block_notfound': '区块信息不存在',
        'address_error': '地址信息查询失败',
        'stat_error' :'统计数据获取失败',
        'chart_error': '图表数据获取失败',
        'search_notfound': '搜索结果不存在',
        'search_error': '获取搜索结果失败',
        'archive_error': '档案数据获取失败',
        'archive_submit_error': '档案信息上传失败',
        'qr_error': '无法产生二维码',
        'logo_error': '无法产生验证码',
        'miner_error': '无法获得矿工信息',
        'node_error': '节点信息获取失败',

    },
    'en': {
        'market_error': 'Oops! Cannot Obtain Market Data',
        'tx_error': 'Invalid Transaction Information',
        'block_error': 'Invalid Block Information',
        'block_notfound': 'No Block Information Found',
        'address_error': 'Invalid Address Information',
        'stat_error': 'Invalid Statistics',
        'chart_error': 'Invalid Chart Data',
        'search_notfound': 'No Pattern Found',
        'search_error': 'Oops! Search Error!',
        'about_error': 'No Related Docs Found',
        'archive_error': 'Invalid Archive Information',
        'archive_submit_error': 'Invalid Data. Cannot Submit Archive',
        'qr_error': 'Cannot Generate QR Code',
        'logo_error': 'Cannot Generate Captcha Image',
        'miner_error': 'Invaild Miner Information',
        'node_error': 'No Nodes Information',

    }
}

ADDRESS_42_RE = re.compile('bm1[02-9ac-hj-np-z]{39}\\Z')
ADDRESS_62_RE = re.compile('bm1[02-9ac-hj-np-z]{59}\\Z')


def wrap_response(data='', status='success', code='200', message='', **kwargs):
    return dict(status=status, data=data, code=code, message=message)


def wrap_ordin_response(status, uri, found=None):
    if status == 200:
        return wrap_ordin_200_response(found, uri)
    elif status == 404:
        return wrap_ordin_404_response(uri)
    elif status == 400:
        return wrap_ordin_400_response(uri)
    else:
        return None


def wrap_ordin_400_response(uri):
    response = {
        "uri": uri,
        "utc": time.time(),
        "status_code": "400",
        "status_detail": "Bad Request",
        "metainfo": {
           "content_type": "text/html",
           "content_length": 51,
         },

        "content": "<html><font color='#F00'>Bad Request</font></html>"
      }
    return response


def wrap_ordin_404_response(uri):
    response = {
        "uri": uri,
        "utc": time.time(),
        "status_code": "404",
        "status_detail": "Not Found",
        "metainfo": {
           "content_type": "text/html",
           "content_length": 49,
         },

        "content": "<html><font color='#F00'>Not Found</font></html>"
      }
    return response


def wrap_ordin_200_response(found, uri):
    content = json.dumps(found)
    metainfo = {
        'content_type': 'text/json',
        'content_length': len(content)
    }
    response = {
        'uri': uri,
        'utc': time.time(),
        'status_code': '200',
        'status_detal': '0K',
        'metainfo': metainfo,
        'content': content
    }
    return response


def wrap_error_response(message='', data='', status='failure', code='500'):
    lang = g.lang if g.get('lang', None) else 'zh'
    response = ERROR_MSG[lang][message]
    print response
    return dict(status=status, data=data, code=code, message=response)


def valid_addr(addr):
    addr.strip().lower()
    return (ADDRESS_42_RE.match(addr) or ADDRESS_62_RE.match(addr)) is not None

