# -*- coding: utf-8 -*-
from flask_restful import Api

import address
import asset
import block
import odin
import search
import service
import stat
import tx


# modules = [(handle, urls, args)]
MODULES = [
    (address.api.AddressAPI, ('/api/address/<string:address>',), {'endpoint': 'address'}),

    (tx.api.TxAPI, ('/api/tx/<string:tx_hash>',), {'endpoint': 'tx'}),
    (tx.api.TxListAPI, ('/api/txs',), {'endpoint': 'txs'}),

    (block.api.BlockAPI, ('/api/block/<string:block_id>',), {'endpoint': 'block'}),
    (block.api.BlockListAPI, ('/api/blocks',), {'endpoint': 'blocks'}),

    (search.api.SearchAPI, ('/api/search',), {'endpoint': 'search'}),

    (stat.api.ChainStatsAPI, ('/api/chain-stats',), {'endpoint': 'chain-stats'}),
    (stat.api.NodeStatsAPI, ('/api/node-stats',), {'endpoint': 'node-stats'}),

    (odin.api.OdinAPI, ('/api/odin',), {'endpoint': 'odin'}),

    (asset.api.AssetAPI, ('/api/asset/<string:asset_id>',), {'endpoint': 'asset'}),
    (asset.api.AssetListAPI, ('/api/assets',), {'endpoint': 'assets'}),


    # Service API
    (service.api.BytomChainAPI, ('/api/v1/chain/<string:chain_api>',), {'endpoint': 'chain_api'}),
    (service.api.BytomBlockAPI, ('/api/v1/block/<string:chain_api>',), {'endpoint': 'block_api'}),
    (service.api.BytomAddressAPI, ('/api/v1/address/<string:chain_api>',), {'endpoint': 'address_api'}),
    (service.api.BytomTxAPI, ('/api/v1/tx/<string:chain_api>',), {'endpoint': 'tx_api'}),
]


def register_api(app):
    api = Api(app)
    for handle, urls, args in MODULES:
        api.add_resource(handle, *urls, **args)
