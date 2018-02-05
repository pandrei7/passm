from cryptography.fernet import Fernet

import esocrypt as es
import random
import string

FIELD_CRYPT_KEY = r'C8kQQtbFrOM!mf4SjdqU4p)K\iV9knyfG O!Wlrk2MPDfcSCduDT68L!v%yBR>KTe\1JNj3N4xPcALm2VXEUCyy6EvDW9aPu4'


def field_crypt_key():
  return es.decrypt(FIELD_CRYPT_KEY)


def random_fernet_key():
  return Fernet.generate_key().decode('utf8')


def random_password(length=64, lower=True, upper=True, digits=True, punct=True):
  chars = ''
  chars += string.ascii_lowercase if lower else ''
  chars += string.ascii_uppercase if upper else ''
  chars += string.digits if digits else ''
  chars += string.punctuation if punct else ''

  if len(chars) <= 0:
    return ''
  return ''.join(random.choices(chars, k=length))


def encrypt_data(key, data):
  key = key.encode('utf8')
  text = data.encode('utf8')
  f = Fernet(key)
  return f.encrypt(text).decode('utf8')


def encrypt_field(data):
  return encrypt_data(field_crypt_key(), data)


def decrypt_data(key, data):
  key = key.encode('utf8')
  text = data.encode('utf8')
  f = Fernet(key)
  return f.decrypt(text).decode('utf8')


def decrypt_field(data):
  return decrypt_data(field_crypt_key(), data)
