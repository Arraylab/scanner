from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5
import base64


def rsa_sign(data):
    private_key_file = open('./blockmeta/key/priv_key.pem', 'r')
    # private_key_file = open('priv_key.pem', 'r')
    pri_key = RSA.importKey(private_key_file.read())
    signer = PKCS1_v1_5.new(pri_key)
    hash_obj = my_hash(data)
    signature = base64.b64encode(signer.sign(hash_obj))
    private_key_file.close()
    return signature


def rsa_verify(signature, data):
    public_key_file = open('./blockmeta/key/pub_key.pem', 'r')
    # public_key_file = open('priv_key.pem', 'r')
    pub_key = RSA.importKey(public_key_file.read())
    hash_obj = my_hash(data)
    verifier = PKCS1_v1_5.new(pub_key)
    public_key_file.close()
    return verifier.verify(hash_obj, base64.b64decode(signature))


def my_hash(data):
    return MD5.new(data.encode('utf-8'))


if __name__ == '__main__':
    data = 'BYTOM'
    signature = rsa_sign(data)
    # NlyvRu56kbkJl2/Vi1dGbs+VISMcOfAB1HDaOgmUB+zZKg6vW1se+jfsZGH/LACXRVcpCnYls2CGgO63LdTZ+uKGkk71o5gF8fZ0QfV9Hil4jXrOLADB/Q4JAQ/QRp75E0yEu1tSZ3cijiRYNGyqI9QGtjbI2w/N9+A7VrXB0ZI=
    print signature
    print rsa_verify(signature, data)
