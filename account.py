import secrets

class Account():
  """ Model the account of a user as it is kept in the database. """

  __slots__ = ['name', 'email', 'username', 'password']

  def __init__(self, name, email, username, password):
    """ Initialize all fields. """
    self.name = name
    self.email = email
    self.username = username
    self.password = password

  def db_data(self):
    """ Return account data as a tuple.

    The order of the fields is the same as in the database.
    """
    return (self.name, self.email, self.username, self.password)


def create_account(name, email, username, password, us):
  """ Return an Account object from the parameters.

  :param name: the account name
  :param email: the account email
  :param username: the account username
  :param password: the account password in plaintext
  :param us: the User who owns the account
  :returns: an Account with encrypted password
  """
  key = secrets.decrypt_field(us.crypt_key)
  password = secrets.encrypt_data(key, password)
  return Account(name, email, username, password)

def unpack(acc_tuple):
  """ Return an Account object from a tuple. """
  return Account(acc_tuple[0], acc_tuple[1], acc_tuple[2], acc_tuple[3])

