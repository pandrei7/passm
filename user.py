import secrets

class User():
  """ Model a user as it is kept in the database. """

  __slots__ = ['name', 'password', 'crypt_key']

  def __init__(self, name, password, crypt_key):
    """ Initialize all fields. """
    self.name = name
    self.password = password
    self.crypt_key = crypt_key

  def db_data(self):
    """ Return user data as a tuple.

    The order of the fields is the same as in the database.
    """
    return (self.name, self.password, self.crypt_key)


def create_user(name, password):
  """ Return a User object from the parameters.

  A random encryption key for the user's account database 
  is generated automatically.

  :param name: the user's name
  :param password: the user's password
  """
  password = secrets.encrypt_field(password)
  crypt_key = secrets.encrypt_field(secrets.random_fernet_key())
  return User(name, password, crypt_key)


def unpack(us_tuple):
  """ Return a User object from a tuple. """
  return User(us_tuple[0], us_tuple[1], us_tuple[2])

