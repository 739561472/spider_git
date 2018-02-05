import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from config import PUBKEY

public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5lalja
N9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7P
AzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQ
q+CA6agNkqly2H4j6wIDAQAB
-----END PUBLIC KEY-----'''
# public_key = '''-----BEGIN PUBLIC KEY-----
# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCBWNoG5LJ3u44Gs8PWs1MaNUQQ
# +mOmh+9zWdzSt3ORbmfCDvU+ssW/6QTTgXvWWx7+Wzq/a4fCCQp72zSqXeVhWkTV
# ct9Hyp/iMo5K6qOEK76z9z+tP/u99X6qazeXGVMWKkPiyZT4mKAGd/U8Mph9Z1Z5
# kOluA7g7heq8PPlE9wIDAQAB
# -----END PUBLIC KEY-----'''


def JSEncrypt(pwd):
    rsakey = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsakey)
    nloginpwd = base64.b64encode(cipher.encrypt(pwd.encode('utf-8')))
    return nloginpwd


JSEncrypt()
