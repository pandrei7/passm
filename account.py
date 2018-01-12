import secrets

class Account():
  __slots__ = ['name', 'email', 'username', 'password']

  def __init__(self, name, email, username, password):
    self.name = name
    self.email = email
    self.username = username
    self.password = password

  def db_data(self):
    return (self.name, self.email, self.username, self.password)


def create_account(name, email, username, password, us):
  key = secrets.decrypt_field(us.crypt_key)
  password = secrets.encrypt_data(key, password)
  return Account(name, email, username, password)

def unpack(acc_tuple):
  return Account(acc_tuple[0], acc_tuple[1], acc_tuple[2], acc_tuple[3])
