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
    (blockmeta.address.api.AddressAPI, ('/api/v1/address/<string:address>',), {'endpoint': 'address'}),

    (blockmeta.tx.api.TxAPI, ('/api/v1/tx/<string:tx_hash>',), {'endpoint': 'tx'}),
    (blockmeta.tx.api.TxListAPI, ('/api/v1/txs',), {'endpoint': 'txs'}),

    (blockmeta.block.api.BlockAPI, ('/api/v1/block/<string:block_id>',), {'endpoint': 'block'}),
    (blockmeta.block.api.BlockListAPI, ('/api/v1/blocks',), {'endpoint': 'blocks'}),

    (blockmeta.search.api.SearchAPI, ('/api/v1/search',), {'endpoint': 'search'}),

    (blockmeta.stat.api.ChainStatsAPI, ('/api/v1/chain-stats',), {'endpoint': 'chain-stats'}),
    (blockmeta.stat.api.NodeStatsAPI, ('/api/v1/node-stats',), {'endpoint': 'node-stats'}),


    (blockmeta.odin.api.OdinAPI, ('/api/v1/odin',), {'endpoint': 'odin'}),

    (blockmeta.asset.api.AssetAPI, ('/api/v1/asset/<string:asset_id>',), {'endpoint': 'asset'}),
    (blockmeta.asset.api.AssetListAPI, ('/api/v1/assets',), {'endpoint': 'assets'})
]


def register_api(app):
    api = Api(app)
    for handle, urls, args in MODULES:
        api.add_resource(handle, *urls, **args)
