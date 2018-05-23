import json
import time
from sign import rsa_sign


def wrap_data(data):
    j_data = json.dumps(data)
    response = {
        'ver': 1,
        'data': j_data,
        'sign': 'MD5withRSA:' + rsa_sign(j_data),
    }

    return response


def parse_next_response(uri):
    r_content = {
        'uri': uri,
        'ver': 1,
        'auth': '0',
        'titile': 'demo',
        'vd_set': {
            'algo': 'MD5withRSA',
            'pubkey': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChNn3wKRtPmxaKq2dKsfMn6sO6AKxvtxZgNdh7\r\nHBWq2z0AJusZHFx2tO2X3jpaYWSIwDrH6AdU2LMMc7IRaUgvLRgT6kPK5OLEzvS+Bmh+1kh7Fz4z\r\nk96UX7UDt55vyK18dJxad+tYwzcN4/Vjudy9RQy6nVX+tRtqRMVNKE254wIDAQAB\r\n',
        },
        'ap_set': {
            '0': {
                'url': 'http://127.0.0.1:5000/api/odin'
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
           "content_length": 51,
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
