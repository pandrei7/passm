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


def create_account(name, email, username, password):
  password = secrets.encrypt_field(password)
  return Account(name, email, username, password)
