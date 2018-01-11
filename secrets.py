from binascii import hexlify

import esocrypt as es
import random
import simplecrypt as sc
import string

FILE_CRYPT_KEY = "R5zDuzSfahgzSt8W~i]Gze^zdDw6eqH2L&foyhBj2ncAtbdnjymIy7Z'EzSoUvF{Cz8L(DtGqm[kcp]3Yg"
FIELD_CRYPT_KEY = 'D1fClnCoF(Zuw~7N~fhPyekV!rx6qcRtbym[jyc`6g_bqbyE giW{5r"PqegezCfKq1aks~IcKfv~br8xgFuFmW Xpe]5NwFjW%k`lgon3Sh'


def file_crypt_key():
  return es.decrypt(FILE_CRYPT_KEY)


def field_crypt_key():
  return es.decrypt(FIELD_CRYPT_KEY)


def random_password(length=64, lower=True, upper=True, digits=True, punct=True):
  chars = ''
  chars += string.ascii_lowercase if lower else ''
  chars += string.ascii_uppercase if upper else ''
  chars += string.digits if digits else ''
  chars += string.punctuation if punct else ''
  return ''.join(random.choices(chars, k=length))


def encrypt_field(data):
  text = data.encode('utf8')
  text = sc.encrypt(field_crypt_key(), text)
  return str(hexlify(text))
