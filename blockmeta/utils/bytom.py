# -*- coding: utf-8 -*-

import re

ADDRESS_RE = re.compile('bm[0-9A-Za-z]{40,60}\\Z')
HASH_PREFIX_RE = re.compile('[0-9a-fA-F]{0,64}\\Z')
HASH_PREFIX_MIN = 6
INIT_BTM = 140700041250000000
INIT_AWARD = 41250000000
EPOCH_LENGTH = 840000


def is_address(s):
    return ADDRESS_RE.match(s)


def is_hash_prefix(s):
    ss = remove_0x(s)
    return HASH_PREFIX_RE.match(ss)


def remove_0x(s):
    return s[2:] if s.startswith("0x") else s


def format_bytom_neu(value):
    return long(value) / (10 ** 8)


def check_block_info(block_info):
    if block_info.isdigit():
        return 'HEIGHT'
    elif is_hash_prefix(block_info):
        return 'HASH'
    return None


def get_total_btm(height):
    epoch = height // EPOCH_LENGTH
    total_num = 0
    for n in range(epoch + 1):
        award = INIT_AWARD / (n + 1)
        total_num += award * (height - n * EPOCH_LENGTH)

    total_num += INIT_BTM
    return total_num
