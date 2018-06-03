#! /usr/bin/env python
# -*- coding: utf-8 -*-


class BytomConf:
    CHAIN_APIS = ['getdifficulty', 'getblockcount', 'lastblockhash', 'reward',
                  'totalbtc', 'avgtxnum', 'interval', 'hashrate', 'nextdifficulty',
                  'unconfirmedcount', 'chainsize', 'lastminer', '24hrpoolstat',
                  '24hrblockcount', 'ticker']

    BLOCK_APIS = ['info', 'tx']

    TX_APIS = ['info', ]

    ADDR_APIS = ['info', 'unconfirmed', 'unspent']

    MISC_APIS = ['hashtoaddress', 'addresstohash', 'difftonethash', 'nethashtodiff',
                 'nbitstodiff', 'difftonbits', 'pushtx']
