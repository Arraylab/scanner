# -*- coding: utf-8 -*-

import json
import os
import platform


def data_dir():
    home_dir = os.environ['HOME']
    sysstr = platform.system()
    if sysstr == 'Darwin':
        path = os.path.join(home_dir, "Library", "Bytom")
    elif sysstr == 'Windows':
        path = os.path.join(home_dir, "AppData", "Roaming", "Bytom")
    else:
        path = os.path.join(home_dir, ".bytom")
    return path


# path: addrbook.json
def read_addr_book(path):
    with open(path, 'r') as f:
        data = json.load(f)
    if data is None:
        return None
    return data['Addrs']


# (ip, port)
def parse_address(path):
    addrs = read_addr_book(path)
    hosts = []
    for item in addrs:
        ip = item['Addr'].get('IP')
        port = item['Addr'].get('Port')
        if ip is None and port is None:
            return None
        hosts.append((ip, port))
    return hosts


def record_to_file(data, filename):
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists('vnode.json'):
        os.system(r'touch {}'.format(filename))
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    from proxy import DbProxy
    proxy = DbProxy()
    pass
