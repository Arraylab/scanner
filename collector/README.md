# data collections in mongodb
## address_info
```
{
	"_id": ObjectId("5b0510090a0c168f0a75f46c"),
	"address": "sm1qwlfuuetehufss9vjr9jpmnsg2zuwv442ppgdyp",
	"asset_balances": {
		"45af88310084188360f5aa2e6f42672671698b82505dd89a1be9164c6f42ef41": {
			"balance": NumberLong("80000000000"),
			"recv": NumberLong("80000000000"),
			"sent": 0
		}
	},
	"balance": 0,
	"block_hash": "4e53522638a8e30822b7ec8732d8c5dc130486d0f95972ea19ab53b22aaec97d",
	"block_height": 1390,
	"recv": 0,
	"sent": 0,
	"txs": ["c226c397d47e9f75d2444a9d10c128089dad104c9e49c7e6d4e29836515cd862"]
}
```
## asset_info
```
{
	"_id": ObjectId("5b050fad0a0c168f0a75f3b2"),
	"asset_id": "45af88310084188360f5aa2e6f42672671698b82505dd89a1be9164c6f42ef41",
	"amount": NumberLong("100000000000"),
	"asset_definition": {},
	"balances": {
		"sm1qwlfuuetehufss9vjr9jpmnsg2zuwv442ppgdyp": NumberLong("80000000000")
	},
	"block_hash": "4e53522638a8e30822b7ec8732d8c5dc130486d0f95972ea19ab53b22aaec97d",
	"block_height": 1390,
	"code": ["TXSIGHASH ", "DATA_32 83221a6da70084312dfecf93273d389b7091ad8430f7ed127e17f652c2d2a559", "1 01", "1 01", "CHECKMULTISIG "],
	"issuance_program": "ae2083221a6da70084312dfecf93273d389b7091ad8430f7ed127e17f652c2d2a5595151ad",
	"issue_by": "415a69c5537c43942c90bbad64c231a1074f69515925b1e600abff3fdd3184ac",
	"retire": NumberLong("20000000000"),
	"txs": ["415a69c5537c43942c90bbad64c231a1074f69515925b1e600abff3fdd3184ac", "c226c397d47e9f75d2444a9d10c128089dad104c9e49c7e6d4e29836515cd862"]
}
```
## block_info
```
{
	"_id": ObjectId("5b05084da033405d9c2feb98"),
	"nonce": NumberLong("9253507043297"),
	"hash": "a75483474799ea1aa6bb910a1a5025b4372bf20bef20f246a2c2dc5e12e8a053",
	"transaction_status_hash": "c9c377e5192668bc0a367e4a4764f11e7c725ecced1d7b6a492974fab1b6d5bc",
	"timestamp": 1524549600,
	"transactions": [{
		"inputs": [{
			"asset_id": "0000000000000000000000000000000000000000000000000000000000000000",
			"asset_definition": {},
			"amount": 0,
			"type": "coinbase",
			"arbitrary": "496e666f726d6174696f6e20697320706f7765722e202d2d204a616e2f31312f323031332e20436f6d707574696e6720697320706f7765722e202d2d204170722f32342f323031382e"
		}],
		"outputs": [{
			"asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
			"code": ["DUP ", "HASH160 ", "DATA_20 8c9d063ff74ee6d9ffa88d83aeb038068366c4c4", "EQUALVERIFY ", "TXSIGHASH ", "SWAP ", "CHECKSIG "],
			"control_program": "00148c9d063ff74ee6d9ffa88d83aeb038068366c4c4",
			"asset_definition": {},
			"amount": NumberLong("140700041250000000"),
			"address": "sm1q3jwsv0lhfmndnlag3kp6avpcq6pkd3xyxg7z8f",
			"position": 0,
			"type": "control",
			"id": "e3325bf07c4385af4b60ad6ecc682ee0773f9b96e1cfbbae9f0f12b86b5f1093"
		}],
		"status_fail": false,
		"time_range": 0,
		"version": 1,
		"id": "158d7d7c6a8d2464725d508fafca76f0838d998eacaacb42ccc58cfb0c155352",
		"size": 151
	}],
	"miner": "sm1q3jwsv0lhfmndnlag3kp6avpcq6pkd3xyxg7z8f",
	"hash_rate": -1,
	"height": 0,
	"difficulty": "15154807",
	"version": 1,
	"previous_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",
	"transaction_merkle_root": "58e45ceb675a0b3d7ad3ab9d4288048789de8194e9766b26d8f42fdb624d4390",
	"bits": NumberLong("2161727821137910632"),
	"size": 546
}
```
## transaction_info
```
{
	"_id": ObjectId("5b05084da033405d9c2feb99"),
	"inputs": [{
		"asset_id": "0000000000000000000000000000000000000000000000000000000000000000",
		"asset_definition": {},
		"amount": 0,
		"type": "coinbase",
		"arbitrary": "496e666f726d6174696f6e20697320706f7765722e202d2d204a616e2f31312f323031332e20436f6d707574696e6720697320706f7765722e202d2d204170722f32342f323031382e"
	}],
	"outputs": [{
		"asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
		"code": ["DUP ", "HASH160 ", "DATA_20 8c9d063ff74ee6d9ffa88d83aeb038068366c4c4", "EQUALVERIFY ", "TXSIGHASH ", "SWAP ", "CHECKSIG "],
		"control_program": "00148c9d063ff74ee6d9ffa88d83aeb038068366c4c4",
		"asset_definition": {},
		"amount": NumberLong("140700041250000000"),
		"address": "sm1q3jwsv0lhfmndnlag3kp6avpcq6pkd3xyxg7z8f",
		"position": 0,
		"type": "control",
		"id": "e3325bf07c4385af4b60ad6ecc682ee0773f9b96e1cfbbae9f0f12b86b5f1093"
	}],
	"status_fail": false,
	"time_range": 0,
	"block_hash": "a75483474799ea1aa6bb910a1a5025b4372bf20bef20f246a2c2dc5e12e8a053",
	"version": 1,
	"block_height": 0,
	"id": "158d7d7c6a8d2464725d508fafca76f0838d998eacaacb42ccc58cfb0c155352",
	"size": 151
}
```