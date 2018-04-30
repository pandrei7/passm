import os
import sqlite3

import user
import utils

class AccountExistsException(Exception):
  """ Signal that an account already exists when it should not. """

  def __init__(self, name):
    """ Initialize the object. """
    Exception.__init__(self, 'Account with name "' + name + '" already exists')


def get_db_path(us):
  """ Return the absolute path of the user's database. """
  return utils.get_resource_path('dbs', us.name + '.db')


def create_database(us):
  """ Create the user's database if it does not exist. """
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (name text, email text, username text, password text);''')


def delete_database(us):
  """ Delete the user's database. """
  try:
    os.remove(get_db_path(us))
  except:
    pass


def get_accounts_by_name_exact(us, name):
  """ Return all accounts which have the exact name. """
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE name LIKE ?;', (name,))
    return c.fetchall()


def get_accounts_by_name(us, name):
  """ Return all accounts whose names contain a word.

  :param us: the User who owns the accounts
  :param name: the word that is searched
  """
  query_string = '%' + name + '%'
  return get_accounts_by_name_exact(us, query_string)


def get_all_accounts(us):
  """ Return all the accounts in the user's database. """
  return get_accounts_by_name(us, '')


def insert_account(us, acc):
  """ Insert a new account in the user's database.

  :param us: the User who owns the database
  :param acc: the new Account
  :raises AccountExistsException: if the account already exists
  """
  if get_accounts_by_name_exact(us, acc.name):
    raise AccountExistsException(acc.name)

  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('INSERT INTO accounts VALUES(?,?,?,?);', acc.db_data())
    conn.commit()


def delete_account(us, acc):
  """ Delete an account from the user's database. """
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''DELETE FROM accounts
                 WHERE name=? AND email=?
                 AND username=? AND password=?;''', acc.db_data())
    conn.commit()


def update_account_data(us, acc):
  """ Update an existing account's data. """
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''UPDATE accounts
                 SET name=?, email=?, username=?, password=?
                 WHERE name=?''', (*acc.db_data(), acc.name))
    conn.commit()


def change_account(us, acc):
  """ Change an existing account or insert a new one. """
  try:
    insert_account(us, acc)
  except AccountExistsException:
    update_account_data(us, acc)

