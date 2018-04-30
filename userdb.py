import os
import sqlite3

import secrets
import user
import utils

class UserExistsException(Exception):
  """ Signal that a user exists when it shouldn't. """

  def __init__(self, name):
    """ Initialize the object. """
    Exception.__init__(self, 'User with name "' + name + '" already exists')


class UserNotFoundException(Exception):
  """ Signal that a requested user was not found. """

  def __init__(self, name):
    """ Initialize the object. """
    Exception.__init__(self, 'User with name "' + name + '" not found')


# The path of the 'dbs' directory
DB_DIR = utils.get_resource_path('dbs')

# The name of the users database
DB_NAME = '.supercalifragilistic'

# The full path of the users database
DB_PATH = utils.get_resource_path(DB_DIR, DB_NAME + '.db')


def create_database():
  """ Create the users database if it does not exist.

  The 'dbs' directory is also created, if needed.
  """
  os.makedirs(DB_DIR, exist_ok=True)
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name text, password text, crypt_key text);''')


def get_users_by_name_exact(name):
  """ Return all users who have the exact name. """
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE name LIKE ?;', (name,))
    return c.fetchall()


def get_users_by_name(name):
  """ Return all users whose name contain a substring.

  :param name: the substring that is searched
  """
  query_string = '%' + name + '%'
  return get_users_by_name_exact(query_string)


def user_exists(name):
  """ Check if a user with a given name exists. """
  present = get_users_by_name_exact(name)
  return len(present) > 0


def insert_user(us):
  """ Insert a new user in the users database.

  :param us: the new User
  :raises UserExistsException: if the user already exists
  """
  if user_exists(us.name):
    raise UserExistsException(us.name)

  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES(?,?,?);', us.db_data())
    conn.commit()


def delete_user(us):
  """ Delete a user from the users database. """
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''DELETE FROM users
                 WHERE name=? AND password=?
                 AND crypt_key=?;''', us.db_data())
    conn.commit()


def check_password(name, password):
  """ Check if a user's password matches a candidate password.

  :param name: the name of the user
  :param password: the candidate password
  :raises UserNotFoundException: if the requested user cannot be found
  """
  us = get_users_by_name_exact(name)
  if not us:
    raise UserNotFoundException(name)

  us = user.unpack(us[0])
  return password == secrets.decrypt_field(us.password)

