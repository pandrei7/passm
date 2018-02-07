import secrets

class User():
  __slots__ = ['name', 'password', 'crypt_key']

  def __init__(self, name, password, crypt_key):
    self.name = name
    self.password = password
    self.crypt_key = crypt_key

  def db_data(self):
    return (self.name, self.password, self.crypt_key)


def create_user(name, password):
  password = secrets.encrypt_field(password)
  crypt_key = secrets.encrypt_field(secrets.random_fernet_key())
  return User(name, password, crypt_key)


def unpack(us_tuple):
  return User(us_tuple[0], us_tuple[1], us_tuple[2])

