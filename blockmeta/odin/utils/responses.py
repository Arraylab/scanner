import json
import time
from sign import rsa_sign, key_dir, sign_algorithm


def wrap_data(data):
    j_data = json.dumps(data)
    response = {
        'ver': 1,
        'data': j_data,
        'sign': sign_algorithm + ':' + rsa_sign(j_data),
    }
    return response


def parse_next_response(uri, next_url='http://127.0.0.1:5000/api/odin'):
    with open(key_dir, 'r') as key_file:
        key_dict = json.load(key_file)
    pubkey = key_dict.get('RSAPublicKey')

    r_content = {
        'uri': uri,
        'ver': 1,
        'auth': '0',
        'titile': 'demo',
        'vd_set': {
            'algo': sign_algorithm,
            'pubkey': pubkey
        },
        'ap_set': {
            '0': {
                'url': next_url
            }
        }
    }
    content = json.dumps(r_content)
    data = {
        "uri": uri,
        "utc": int(time.time()),
        "status_code": "200",
        "status_detail": "Ok",
        "metainfo": {
           "content_type": "text/json",
           "content_length": len(content),
         },

        "content": content
    }

    response = wrap_data(data)
    return response


def hello_world_response(uri):
    with open('./blockmeta/odin/resource/home.html', 'r') as f:
        content = f.read()
    data = {
        "uri": uri,
        "utc": int(time.time()),
        "status_code": "200",
        "status_detail": "Ok",
        "metainfo": {
           "content_type": "text/html",
           "content_length": len(content),
         },

        "content": content
      }

    response = wrap_data(data)
    return response


def wrap_ordin_response(status, uri, found=None):
    if status == 200:
        return wrap_ordin_200_response(found, uri)
    elif status == 404:
        return wrap_ordin_404_response(uri)
    elif status == 400:
        return wrap_ordin_400_response(uri)
    else:
        return None


def wrap_ordin_400_response(uri):
    data = {
        "uri": uri,
        "utc": int(time.time()),
        "status_code": "400",
        "status_detail": "Bad Request",
        "metainfo": {
           "content_type": "text/html",
           "content_length": 51,
         },

        "content": "<html><font color='#F00'>Bad Request</font></html>"
      }

    response = wrap_data(data)
    return response


def wrap_ordin_404_response(uri):
    data = {
        "uri": uri,
        "utc": int(time.time()),
        "status_code": "404",
        "status_detail": "Not Found",
        "metainfo": {
           "content_type": "text/html",
           "content_length": 49,
         },

        "content": "<html><font color='#F00'>Not Found</font></html>"
      }

    response = wrap_data(data)
    return response


def wrap_ordin_200_response(found, uri):
    content = json.dumps(found)
    metainfo = {
        'content_type': 'text/json',
        'content_length': len(content)
    }
    data = {
        'uri': uri,
        'utc': int(time.time()),
        'status_code': '200',
        'status_detal': '0K',
        'metainfo': metainfo,
        'content': content
    }
    response = wrap_data(data)
    return response
