testTable = testTable2
testTable = testTable1
agent.sync_block(BLOCK_A_02, 3)


agent.sync_block(BLOCK_A, 0)
agent.sync_block(BLOCK_A_00, 1)
agent.sync_block(BLOCK_A_11, 2)
agent.sync_block(BLOCK_A_02, 3)

testTable1 = {0:BLOCK_A, 1: BLOCK_A_00, 2: BLOCK_A_01, 3: BLOCK_A_02}
testTable2 = {0:BLOCK_A, 1: BLOCK_A_10, 2: BLOCK_A_11}


COINBASE = {
    "id": "COINBASE", 
    "version": 1, 
    "size": 78, 
    "time_range": 0, 
    "inputs": [
        {
            "type": "coinbase", 
            "asset_id": "GOD", 
            "asset_definition": { }, 
            "amount": 0, 
            "arbitrary": "test"
        }
    ], 
    "outputs": [
        {
            "type": "control", 
            "id": "400cfcfd02cb8d64fca23c905ee76855e34883979c762b2e55bba3cd4002b645", 
            "position": 0, 
            "asset_id": "BYTOM", 
            "asset_definition": { }, 
            "amount": 10, 
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1", 
            "address": "MINER"
        }
    ], 
    "status_fail": False
}



TX1 = {
    "id": "TX1",
    "version": 1,
    "size": 2124,
    "time_range": 0,
    "inputs": [
        {
            "type": "spend",
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 4,
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
            "address": "JASON",
            "spent_output_id": "00f0d7725604d48cf36d93df91dd9cfae75feef2baa68d4cf7feaac392e166df"
        }
       
    ],
    "outputs": [
        {
            "type": "control",
            "id": "625a946279d691e6e752f0fc39d550f06fa710d8b5b8df55017ea628919eb20a",
            "position": 0,
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 2,
            "control_program": "0014180042c19a9ed564bbbd6aa63a14f4d865d03e0a",
            "address": "KARMEN"
        }
    ],
    "status_fail": False
}


TX2 = {
    "id": "TX2",
    "version": 1,
    "size": 2124,
    "time_range": 0,
    "inputs": [
        {
            "type": "spend",
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 3,
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
            "address": "JASON",
            "spent_output_id": "00f0d7725604d48cf36d93df91dd9cfae75feef2baa68d4cf7feaac392e166df"
        }
       
    ],
    "outputs": [
        {
            "type": "control",
            "id": "625a946279d691e6e752f0fc39d550f06fa710d8b5b8df55017ea628919eb20a",
            "position": 0,
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 3,
            "control_program": "0014180042c19a9ed564bbbd6aa63a14f4d865d03e0a",
            "address": "KARMEN"
        }
    ],
    "status_fail": False
}

TX3 = {
    "id": "TX3",
    "version": 1,
    "size": 2124,
    "time_range": 0,
    "inputs": [
        {
            "type": "spend",
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 5,
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
            "address": "KARMEN",
            "spent_output_id": "00f0d7725604d48cf36d93df91dd9cfae75feef2baa68d4cf7feaac392e166df"
        }
       
    ],
    "outputs": [
        {
            "type": "control",
            "id": "625a946279d691e6e752f0fc39d550f06fa710d8b5b8df55017ea628919eb20a",
            "position": 0,
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 1,
            "control_program": "0014180042c19a9ed564bbbd6aa63a14f4d865d03e0a",
            "address": "JASON"
        }
    ],
    "status_fail": False
}
TX4 = {
    "id": "TX4",
    "version": 1,
    "size": 2124,
    "time_range": 0,
    "inputs": [
        {
            "type": "spend",
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 5,
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
            "address": "JASON",
            "spent_output_id": "00f0d7725604d48cf36d93df91dd9cfae75feef2baa68d4cf7feaac392e166df"
        }
       
    ],
    "outputs": [
        {
            "type": "control",
            "id": "625a946279d691e6e752f0fc39d550f06fa710d8b5b8df55017ea628919eb20a",
            "position": 0,
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 1,
            "control_program": "0014180042c19a9ed564bbbd6aa63a14f4d865d03e0a",
            "address": "KARMEN"
        }
    ],
    "status_fail": False

}
TX5 = {
    "id": "TX5",
    "version": 1,
    "size": 2124,
    "time_range": 0,
    "inputs": [
        {
            "type": "spend",
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 4,
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
            "address": "JASON",
            "spent_output_id": "00f0d7725604d48cf36d93df91dd9cfae75feef2baa68d4cf7feaac392e166df"
        }
       
    ],
    "outputs": [
        {
            "type": "control",
            "id": "625a946279d691e6e752f0fc39d550f06fa710d8b5b8df55017ea628919eb20a",
            "position": 0,
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 2,
            "control_program": "0014180042c19a9ed564bbbd6aa63a14f4d865d03e0a",
            "address": "JASON"
        }
    ],
    "status_fail": False
}
TX6 = {
    "id": "TX6",
    "version": 1,
    "size": 2124,
    "time_range": 0,
    "inputs": [
        {
            "type": "spend",
            "asset_id": "BYTOM",
            "asset_definition": { },
            "amount": 2,
            "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
            "address": "KARMEN",
            "spent_output_id": "00f0d7725604d48cf36d93df91dd9cfae75feef2baa68d4cf7feaac392e166df"
        }
       
    ],
    "outputs": [
        {
            "type": "control",
            "id": "625a946279d691e6e752f0fc39d550f06fa710d8b5b8df55017ea628919eb20a",
            "position": 0,
            "asset_id": "KARMEN",
            "asset_definition": { },
            "amount": 4,
            "control_program": "0014180042c19a9ed564bbbd6aa63a14f4d865d03e0a",
            "address": "KARMEN"
        }
    ],
    "status_fail": False
}



BLOCK_A = {
    "hash": "BLOCK_A_ID", 
    "size": 4648, 
    "version": 1, 
    "height": 0, 
    "previous_block_hash": "ASK_GOD", 
    "timestamp": 0, 
    "nonce": 0, 
    "bits": 0, 
    "difficulty": "difficulty", 
    "transaction_merkle_root": "transaction_merkle_root", 
    "transaction_status_hash": "transaction_status_hash", 
    "transactions": [COINBASE]
}

BLOCK_A_00 = {
    "hash": "BLOCK_A_00_ID", 
    "size": 4648, 
    "version": 1, 
    "height": 1, 
    "previous_block_hash": "BLOCK_A_ID", 
    "timestamp": 0, 
    "nonce": 0, 
    "bits": 0, 
    "difficulty": "difficulty", 
    "transaction_merkle_root": "transaction_merkle_root", 
    "transaction_status_hash": "transaction_status_hash", 
    "transactions": [COINBASE, TX1, TX2]
}

BLOCK_A_10 = {
    "hash": "BLOCK_A_10_ID", 
    "size": 4648, 
    "version": 1, 
    "height": 1, 
    "previous_block_hash": "BLOCK_A_ID", 
    "timestamp": 0, 
    "nonce": 0, 
    "bits": 0, 
    "difficulty": "difficulty", 
    "transaction_merkle_root": "transaction_merkle_root", 
    "transaction_status_hash": "transaction_status_hash", 
    "transactions": [COINBASE, TX2, TX3]
}

BLOCK_A_11 = {
    "hash": "BLOCK_A_11_ID", 
    "size": 4648, 
    "version": 1, 
    "height": 2, 
    "previous_block_hash": "BLOCK_A_10_ID", 
    "timestamp": 0, 
    "nonce": 0, 
    "bits": 0, 
    "difficulty": "difficulty", 
    "transaction_merkle_root": "transaction_merkle_root", 
    "transaction_status_hash": "transaction_status_hash", 
    "transactions": [COINBASE, TX1, TX5]
}

BLOCK_A_01 = {
    "hash": "BLOCK_A_01_ID", 
    "size": 4648, 
    "version": 1, 
    "height": 2, 
    "previous_block_hash": "BLOCK_A_00_ID", 
    "timestamp": 0, 
    "nonce": 0, 
    "bits": 0, 
    "difficulty": "difficulty", 
    "transaction_merkle_root": "transaction_merkle_root", 
    "transaction_status_hash": "transaction_status_hash", 
    "transactions": [COINBASE, TX3, TX4]
}

BLOCK_A_02 = {
    "hash": "BLOCK_A_02_ID", 
    "size": 4648, 
    "version": 1, 
    "height": 3, 
    "previous_block_hash": "BLOCK_A_01_ID", 
    "timestamp": 0, 
    "nonce": 0, 
    "bits": 0, 
    "difficulty": "difficulty", 
    "transaction_merkle_root": "transaction_merkle_root", 
    "transaction_status_hash": "transaction_status_hash", 
    "transactions": [COINBASE, TX5, TX6]
}




