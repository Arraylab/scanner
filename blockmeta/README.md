# Blockmeta Data API

The Blockmeta Bytom APIs are provided as a community service and without warranty, so please just use what you need no more.
They support both GET/POST requests and a rate limit of 5 requests/sec.


## Address

- http://blockmeta.com/api/address/bm1qcxg0w7c70tdd46t7dxn204mkyeyudcz063s49e
- Optional limit parameter to show n transactions e.g.&limit=50(Default:50, Max:50)(**TODO**)

```
{
    "balance": 22897805292,
    "recv": 22897805292,
    "tx_num": 3,
    "txs": [--Array of Transactions--],
    "asset_balance": {}
    "sent": 0
}
```

## Transaction

### Single Transaction

- http://blockmeta.com/api/tx/7afbc4ddd4ead3e29f73a62e61ac1034e31c7834836c41111d02c5ae77ff9ea9

```
{
    "block_hash": "a75483474799ea1aa6bb910a1a5025b4372bf20bef20f246a2c2dc5e12e8a053",
    "block_height": 0,
    "confirmation": 21400,
    "id": "158d7d7c6a8d2464725d508fafca76f0838d998eacaacb42ccc58cfb0c155352",
    "inputs": [
        {
            "amount": 0,
            "arbitrary": "496e666f726d6174696f6e20697320706f7765722e202d2d204a616e2f31312f323031332e20436f6d707574696e6720697320706f7765722e202d2d204170722f32342f323031382e",
            "asset_definition": {},
            "asset_id": "0000000000000000000000000000000000000000000000000000000000000000",
            "type": "coinbase"
        }
    ],
    "outputs": [
        {
            "address": "bm1q3jwsv0lhfmndnlag3kp6avpcq6pkd3xy8e5r88",
            "amount": 140700041250000000,
            "asset_definition": {},
            "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "code": [
                "DUP",
                "HASH160",
                "DATA_20 8c9d063ff74ee6d9ffa88d83aeb038068366c4c4",
                "EQUALVERIFY",
                "TXSIGHASH",
                "SWAP",
                "CHECKSIG"
            ],
            "control_program": "00148c9d063ff74ee6d9ffa88d83aeb038068366c4c4",
            "id": "e3325bf07c4385af4b60ad6ecc682ee0773f9b96e1cfbbae9f0f12b86b5f1093",
            "position": 0,
            "type": "control"
        }
    ],
    "size": 151,
    "status_fail": false,
    "time_range": 0,
    "version": 1
}
```

### Transaction List

- http://blockmeta.com/api/txs?page=1
- Add total_tx_numb fields(**TODO**)
- Optional limit parameter to show n transactions e.g.&limit=50(Default:50, Max:100)(**TODO**)

```
{
    "code": "200",
    "data": {
        "page": 1,
        "total_page": 2674,
        "txs": [--Array of Transactions--]
    },
    "message": "",
    "status": "success"
}
```

## Block

### Single Block

- http://blockmeta.com/api/block/0

```
{
    "code": "200",
    "data": {
        "block_hash": "a75483474799ea1aa6bb910a1a5025b4372bf20bef20f246a2c2dc5e12e8a053",
        "block_height": 0,
        "block_size": 546,
        "block_version": 1,
        "difficulty": "15154807",
        "nbit": 2161727821137910632,
        "nonce": 9253507043297,
        "pre_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",
        "timestamp": 1524549600,
        "transaction_status_hash": "c9c377e5192668bc0a367e4a4764f11e7c725ecced1d7b6a492974fab1b6d5bc",
        "transactions": [
            {
                "id": "158d7d7c6a8d2464725d508fafca76f0838d998eacaacb42ccc58cfb0c155352",
                "inputs": [
                    {
                        "amount": 0,
                        "arbitrary": "496e666f726d6174696f6e20697320706f7765722e202d2d204a616e2f31312f323031332e20436f6d707574696e6720697320706f7765722e202d2d204170722f32342f323031382e",
                        "asset_definition": {},
                        "asset_id": "0000000000000000000000000000000000000000000000000000000000000000",
                        "type": "coinbase"
                    }
                ],
                "outputs": [
                    {
                        "address": "bm1q3jwsv0lhfmndnlag3kp6avpcq6pkd3xy8e5r88",
                        "amount": 140700041250000000,
                        "asset_definition": {},
                        "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                        "code": [
                            "DUP",
                            "HASH160",
                            "DATA_20 8c9d063ff74ee6d9ffa88d83aeb038068366c4c4",
                            "EQUALVERIFY",
                            "TXSIGHASH",
                            "SWAP",
                            "CHECKSIG"
                        ],
                        "control_program": "00148c9d063ff74ee6d9ffa88d83aeb038068366c4c4",
                        "id": "e3325bf07c4385af4b60ad6ecc682ee0773f9b96e1cfbbae9f0f12b86b5f1093",
                        "position": 0,
                        "type": "control"
                    }
                ],
                "size": 151,
                "status_fail": false,
                "time_range": 0,
                "version": 1
            }
        ],
        "tx_merkle_root": "58e45ceb675a0b3d7ad3ab9d4288048789de8194e9766b26d8f42fdb624d4390"
    },
    "message": "",
    "status": "success"
}
```

### Block List

- http://blockmeta.com/api/blocks?no_page=1

```
{
    "code": "200",
    "data": {
        "blocks": [--Array of Blocks--],
        "no_page": 1,
        "pages": 2495
    },
    "message": "",
    "status": "success"
}
```

## Stats

### Node Stats

- http://blockmeta.com/api/node-stats

```
{
    "code": "200",
    "data": {
        "current_node_num": 7,
        "online_nodes": [
            [
                "47.96.42.1",
                46656
            ],
            [...]
        ],
        "time_lapse": 6.874143838882446,
        "timestamp": 1527231992
    },
    "message": "",
    "status": "success"
}
```

### Chain Stats

- http://blockmeta.com/api/node-stats

```
{
    "code": "200",
    "data": {
        "average_block_fee": 4884778,
        "average_block_interval": 136,
        "average_tx_fee": 1559,
        "block_hash": "d87c637855e30a8a6f7a1c76beeb95c07d59bc81dca88b79e8767c5cbca10676",
        "block_num": 631,
        "hash_rate": 61792861,
        "height": 25023,
        "max_block_interval": 963,
        "median_block_interval": 85,
        "min_block_interval": 5,
        "timestamp": 1527231985,
        "tx_num": 1893
    },
    "message": "",
    "status": "success"
}
```

## Assets

### Single Asset

- http://blockmeta.com/api/asset/{asset-id}?tag='txs'
- http://blockmeta.com/api/asset/{asset-id}?tag='balances'
- Default tag is txs

```
{
    "amount": 10000000000,
    "asset_definition": {},
    "asset_id": "2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214",
    "code": [
        "TXSIGHASH",
        "DATA_32 65a398eff9bc3fdfb920be7e66b1941ccc9df08ebda2e9fec2136124be4f28ed",
        "1 01",
        "1 01",
        "CHECKMULTISIG"
    ],
    "holder_num": 3,
    "info": [--Array of Transactions--],
    "issue_by": "4f1f06175df9aad2a9e2403f376c6a509588a56b0ee995190163640437c7cf0e",
    "issue_timestamp": 1527144206,
    "page": 1,
    "pages": 1,
    "retire": 2000000000,
    "tx_num": 3,
    "update_timestamp": 1527150538
}
```


### Asset List

- http://blockmeta.com/api/assets?page=1

```
{
    "asset_num": 0,
    "assets": [--Array of Transactions--],
    "page": 1,
    "pages": 1
}
```


## TODO

### Stats

- Uniform page field
- Refator Chain Stats(real time, or every 100 Blocks), as follows:
```
{
    "code": "200",
    "data": {
        "height": 20000,
        "block_hash": "d87c637855e30a8a6f7a1c76beeb95c07d59bc81dca88b79e8767c5cbca10676",
        "average_block_interval": 136,
        "max_block_interval": 963,
        "median_block_interval": 85,
        "min_block_interval": 5,
        "average_tx_fee": 1559,
        "time_range": 15000
        "tx_num" 1893
    },
    "message": "",
    "status": "success"
}
```

```
{
    "code": "200",
    "data": {
        "height": 20058
        "hash_rate": 61792861,
        "timestamp": 1527231985,
        "difficuty": "1225071929",
        "price_usd": 1.0

    },
    "message": "",
    "status": "success"
}
```

