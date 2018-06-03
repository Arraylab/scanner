# -*- coding: utf-8 -*-
from flask_restful import Api

import blockmeta.address.api
import blockmeta.block.api
import blockmeta.search.api
import blockmeta.tx.api
import blockmeta.stat.api
import blockmeta.odin.api
import blockmeta.asset.api

# modules = [(handle, urls, args)]
MODULES = [
    (blockmeta.address.api.AddressAPI, ('/api/address/<string:address>',), {'endpoint': 'address'}),

    (blockmeta.tx.api.TxAPI, ('/api/tx/<string:tx_hash>',), {'endpoint': 'tx'}),
    (blockmeta.tx.api.TxListAPI, ('/api/txs',), {'endpoint': 'txs'}),

    (blockmeta.block.api.BlockAPI, ('/api/block/<string:block_id>',), {'endpoint': 'block'}),
    (blockmeta.block.api.BlockListAPI, ('/api/blocks',), {'endpoint': 'blocks'}),

    (blockmeta.search.api.SearchAPI, ('/api/search',), {'endpoint': 'search'}),

    (blockmeta.stat.api.ChainStatsAPI, ('/api/chain-stats',), {'endpoint': 'chain-stats'}),
    (blockmeta.stat.api.NodeStatsAPI, ('/api/node-stats',), {'endpoint': 'node-stats'}),

    (blockmeta.odin.api.OdinAPI, ('/api/odin',), {'endpoint': 'odin'}),

    (blockmeta.asset.api.AssetAPI, ('/api/asset/<string:asset_id>',), {'endpoint': 'asset'}),
    (blockmeta.asset.api.AssetListAPI, ('/api/assets',), {'endpoint': 'assets'})


    # Service API
    (service.BitcoinChainAPI,     ('/api/v1/btc/chain/<string:chain_api>',),      {'endpoint': 'chain_api'})
]


def register_api(app):
    api = Api(app)
    for handle, urls, args in MODULES:
        api.add_resource(handle, *urls, **args)
