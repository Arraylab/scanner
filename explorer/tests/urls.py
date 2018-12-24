#! /usr/bin/env python
# -*- coding: utf-8 -*-

from settings import HOST

api_url = {
    'get_user': '/api/account/user',
    'login': '/api/account/login',
    'change_password': '/api/account/change_password',
    'user_setting': '/api/account/setting',
    'avatar_upload': '/api/account/avatar/upload',
    'avatar_get': '/api/account/avatar',
    'message': '/api/account/message',
    'message_detail': '/api/account/message/detail',
    'message_delete': '/api/account/message/delete',
    'message_statistics': '/api/account/message/statistics',
    'message_restore': '/api/account/message/restore',
    'nickname_search': '/api/account/nick_name/search',
    'captcha': '/api/account/get_captcha',
    'send_code': '/api/account/send_code',
    
    #bitcoin and ethereum urls
    'block_info': '/api/block',
    'token_info': '/api/token',
    'tx_info': '/api/tx',
    'address_info': '/api/address',
    'market_info': '/api/markets',
    'stat_info': '/api/stat',
    'api_info': '/api/v1',
    'miner_info': '/api/miner',
    'qr_info': '/api/qrcode',
    'captcha_info': '/api/captcha',
    'logo_info': '/api/logo',
    'archives_info': '/api/archives',
    'archives_noted_info': '/api/archives',
    'charts_info': '/api/charts',
    'chain_chart_info': '/api/chart/chain',
    'block_chart_info': '/api/chart/block',
    'address_chart_info': '/api/chart/address',
    'block_index_chart_info': '/api/chart/block_index',
    'miner_chart_info': '/api/chart/miner',
    'tx_chart_info': '/api/chart/tx',
    'abouts_info': '/api/abouts',
    'search_info': '/api/search',

}

def get_api_url(param):
    return HOST + api_url[param]