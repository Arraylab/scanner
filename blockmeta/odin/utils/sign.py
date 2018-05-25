from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5
import base64
import json

key_dir = r'./blockmeta/key/keystore.json'
sign_algorithm = 'MD5withRSA'


def rsa_sign(data):
    with open(key_dir, 'r') as key_file:
        key_dict = json.load(key_file)
    pri_key = RSA.importKey(base64.b64decode(key_dict.get('RSAPrivateKey')))
    signer = PKCS1_v1_5.new(pri_key)
    hash_obj = my_hash(data)
    signature = base64.b64encode(signer.sign(hash_obj))
    return signature


def rsa_verify(signature, data):
    with open(key_dir, 'r') as key_file:
        key_dict = json.load(key_file)
    pub_key = RSA.importKey(base64.b64decode(key_dict.get('RSAPublicKey')))
    hash_obj = my_hash(data)
    verifier = PKCS1_v1_5.new(pub_key)
    return verifier.verify(hash_obj, base64.b64decode(signature))


def my_hash(data):
    return MD5.new(data.encode('utf-8'))


if __name__ == '__main__':
    data = 'BYTOM'
    signature = rsa_sign(data)
    # NlyvRu56kbkJl2/Vi1dGbs+VISMcOfAB1HDaOgmUB+zZKg6vW1se+jfsZGH/LACXRVcpCnYls2CGgO63LdTZ+uKGkk71o5gF8fZ0QfV9Hil4jXrOLADB/Q4JAQ/QRp75E0yEu1tSZ3cijiRYNGyqI9QGtjbI2w/N9+A7VrXB0ZI=
    print signature
    print rsa_verify(signature, data)


