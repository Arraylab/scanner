http://127.0.0.1:5000/api/asset/2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214
```
{
    "amount": 10000000000,
    "asset_definition": {},
    "code": [
        "TXSIGHASH",
        "DATA_32 65a398eff9bc3fdfb920be7e66b1941ccc9df08ebda2e9fec2136124be4f28ed",
        "1 01",
        "1 01",
        "CHECKMULTISIG"
    ],
    "holder_num": 2,
    "info": [
        {
            "block_hash": "a76dc57b0094e5bd7470b1011e84d3fbae937041f549e8c043b666a4f538e9eb",
            "block_height": 1459,
            "id": "b30e2e0759d56c6239b2e1351747a97aa5c7f321161f7e185605f5c5e6542f24",
            "inputs": [
                {
                    "address": "sm1qmzscm80frxkla6ew8g56k0743qthxqr3kq6ml4",
                    "amount": 10000000000,
                    "asset_definition": {},
                    "asset_id": "2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214",
                    "control_program": "0014d8a18d9de919adfeeb2e3a29ab3fd58817730071",
                    "spent_output_id": "a9db0ccb8b50dd031003a6954a731ce43eb86fa6a6915fcc29b05b58bb6d4294",
                    "type": "spend"
                },
                {
                    "address": "sm1qpat0qv68yk6vtlppm0377rxxjcmj4x2jhwsnxr",
                    "amount": 41250000000,
                    "asset_definition": {},
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "control_program": "00140f56f0334725b4c5fc21dbe3ef0cc696372a9952",
                    "spent_output_id": "006691efebf53cf387d2d712a7a7cc08943383efbd5cdb900b2be076c6be64b5",
                    "type": "spend"
                }
            ],
            "outputs": [
                {
                    "address": "sm1q7k66mj4a595t50esgvfx7xjznrc64qs9fz4clx",
                    "amount": 5000000000,
                    "asset_definition": {},
                    "asset_id": "2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 f5b5adcabda168ba3f3043126f1a4298f1aa8205",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014f5b5adcabda168ba3f3043126f1a4298f1aa8205",
                    "id": "75b8b5641a6855bea5bf879f029b62b6e36001174c3671a0a68ea7e1ae29ec51",
                    "position": 0,
                    "type": "control"
                },
                {
                    "address": "sm1qhd49u5uxa8w37p3jyd96dfttfcp538ydjezk5z",
                    "amount": 31250000000,
                    "asset_definition": {},
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 bb6a5e5386e9dd1f0632234ba6a56b4e03489c8d",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014bb6a5e5386e9dd1f0632234ba6a56b4e03489c8d",
                    "id": "50d2c887a82355998c812db9ba76211c365ddc57af364f91d64e6085231f74af",
                    "position": 1,
                    "type": "control"
                },
                {
                    "address": "sm1qeckclscyjmld9wrmqkhdwjmtx3zufk8jfun99q",
                    "amount": 3000000000,
                    "asset_definition": {},
                    "asset_id": "2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 ce2d8fc30496fed2b87b05aed74b6b3445c4d8f2",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014ce2d8fc30496fed2b87b05aed74b6b3445c4d8f2",
                    "id": "31dbaac468521fdc7747da534098cc685acba1dd16ea1dd902fd36dbb0a67699",
                    "position": 2,
                    "type": "control"
                },
                {
                    "amount": 2000000000,
                    "asset_definition": {},
                    "asset_id": "2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214",
                    "code": [
                        "FAIL"
                    ],
                    "control_program": "6a",
                    "id": "5da6f01800aba7eceb86a5ce3ae1ccd92ac5606674e038af882d2cd5f5264cdb",
                    "position": 3,
                    "type": "retire"
                },
                {
                    "address": "sm1qeckclscyjmld9wrmqkhdwjmtx3zufk8jfun99q",
                    "amount": 8000000000,
                    "asset_definition": {},
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 ce2d8fc30496fed2b87b05aed74b6b3445c4d8f2",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014ce2d8fc30496fed2b87b05aed74b6b3445c4d8f2",
                    "id": "cd13c6949bee7ba88acdf3b35b0e9d6f11ba0ff13c7059804a3e1dffce1da0cb",
                    "position": 4,
                    "type": "control"
                }
            ],
            "size": 701,
            "status_fail": false,
            "time_range": 0,
            "timestamp": 1527144365,
            "version": 1
        },
        {
            "block_hash": "13bdf32b8087ec46bdbd52094ffa924a54eccfd110fe6f33c6682a71ec4ec25c",
            "block_height": 1363,
            "id": "4f1f06175df9aad2a9e2403f376c6a509588a56b0ee995190163640437c7cf0e",
            "inputs": [
                {
                    "address": "sm1qpat0qv68yk6vtlppm0377rxxjcmj4x2jhwsnxr",
                    "amount": 41250000000,
                    "asset_definition": {},
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "control_program": "00140f56f0334725b4c5fc21dbe3ef0cc696372a9952",
                    "spent_output_id": "000fa7c763f8e2ffbf7431bcb6f34c24b0c6e6c1ed6be2230537997798a59c3f",
                    "type": "spend"
                },
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
                    "issuance_program": "ae2065a398eff9bc3fdfb920be7e66b1941ccc9df08ebda2e9fec2136124be4f28ed5151ad",
                    "type": "issue"
                }
            ],
            "outputs": [
                {
                    "address": "sm1qeckclscyjmld9wrmqkhdwjmtx3zufk8jfun99q",
                    "amount": 31250000000,
                    "asset_definition": {},
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 ce2d8fc30496fed2b87b05aed74b6b3445c4d8f2",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014ce2d8fc30496fed2b87b05aed74b6b3445c4d8f2",
                    "id": "580041eb1af14ffdcdb1dc5104ab429daf71e663b5e18995f9e677e3ed676d34",
                    "position": 0,
                    "type": "control"
                },
                {
                    "address": "sm1qmzscm80frxkla6ew8g56k0743qthxqr3kq6ml4",
                    "amount": 10000000000,
                    "asset_definition": {},
                    "asset_id": "2bd71210029ae842f6a4ac905e73e69462572bbaecdb14e6bed40023459d4214",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 d8a18d9de919adfeeb2e3a29ab3fd58817730071",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014d8a18d9de919adfeeb2e3a29ab3fd58817730071",
                    "id": "a9db0ccb8b50dd031003a6954a731ce43eb86fa6a6915fcc29b05b58bb6d4294",
                    "position": 1,
                    "type": "control"
                },
                {
                    "address": "sm1qmzscm80frxkla6ew8g56k0743qthxqr3kq6ml4",
                    "amount": 9000000000,
                    "asset_definition": {},
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "code": [
                        "DUP",
                        "HASH160",
                        "DATA_20 d8a18d9de919adfeeb2e3a29ab3fd58817730071",
                        "EQUALVERIFY",
                        "TXSIGHASH",
                        "SWAP",
                        "CHECKSIG"
                    ],
                    "control_program": "0014d8a18d9de919adfeeb2e3a29ab3fd58817730071",
                    "id": "ba4e81843f1cf35dcb23dd796428be6d59b992c7707fe32020f451dac74facae",
                    "position": 2,
                    "type": "control"
                }
            ],
            "size": 624,
            "status_fail": false,
            "time_range": 0,
            "timestamp": 1527144206,
            "version": 1
        }
    ],
    "issue_by": "4f1f06175df9aad2a9e2403f376c6a509588a56b0ee995190163640437c7cf0e",
    "issue_timestamp": 1527144206,
    "page": 1,
    "pages": 1,
    "retire": 2000000000,
    "tx_num": 2,
    "update_timestamp": 1527144365
}
```