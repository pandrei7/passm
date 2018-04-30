""" Contain crytographic functions. """

from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64

import esocrypt as es
import random
import string

FIELD_CRYPT_KEY = r'C8kQQtbFrOM!mf4SjdqU4p)K\iV9knyfG O!Wlrk2MPDfcSCduDT68L!v%yBR>KTe\1JNj3N4xPcALm2VXEUCyy6EvDW9aPu4'
DERIVATION_SALT = r'i9f@zkx}mjivbe8OwzldwpmjhS(7O{bhxxN!RvT|2W"y-U"ZQpfF"3ZlzqS#nkBhAy3ChFub|roubAd7IskeurmxK~wZ2Pu'


def field_crypt_key():
  """ Return the crypt-key for fields. """
  return es.decrypt(FIELD_CRYPT_KEY)


def derivation_salt():
  """ Return the derivation salt. """
  return es.decrypt(DERIVATION_SALT)


def random_fernet_key():
  """ Return a random Fernet key. """
  return Fernet.generate_key().decode('utf8')


def random_password(length=64, lower=True, upper=True, digits=True, punct=True):
  """ Return a random password that matches the chosen options. """
  chars = ''
  chars += string.ascii_lowercase if lower else ''
  chars += string.ascii_uppercase if upper else ''
  chars += string.digits if digits else ''
  chars += string.punctuation if punct else ''

  if len(chars) <= 0:
    return ''
  return ''.join(random.choices(chars, k=length))

def derive_fernet_key(password):
  """ Return a Fernet key derived from a normal password. """
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=derivation_salt().encode('utf-8'),
      iterations=100000,
      backend=default_backend()
  )

  password = password.encode('utf-8')
  return base64.urlsafe_b64encode(kdf.derive(password)).decode('utf-8')


def encrypt_data(key, data):
  """ Return the data as an encrypted string. """
  key = key.encode('utf8')
  text = data.encode('utf8')
  f = Fernet(key)
  return f.encrypt(text).decode('utf8')


def encrypt_field(data):
  """ Return the data as a string encrypted like a database field. """
  return encrypt_data(field_crypt_key(), data)


def decrypt_data(key, data):
  """ Return the data as a decrypted string. """
  key = key.encode('utf8')
  text = data.encode('utf8')
  f = Fernet(key)
  return f.decrypt(text).decode('utf8')


def decrypt_field(data):
  """ Return the data as a string decrypted like a database field. """
  return decrypt_data(field_crypt_key(), data)

