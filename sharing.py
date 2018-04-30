""" Contain functions for importing and exporting account databases. """

import sqlite3

import account
import accountdb
import secrets
import user

def create_sharing_database(path):
  """ Create a database that can be shared at the specified path. 
  
  If the database already exists, it is overwritten.
  """
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS accounts;''')
    c.execute('''CREATE TABLE accounts
                 (name text, email text, username text, password text);''')


def populate_sharing_database(path, acc):
  """ Populate a database with accounts.

  :param path: the path of the database
  :param acc: a list including all the accounts to be inserted
  """  
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    for a in acc:
      c.execute('''INSERT INTO accounts VALUES (?, ?, ?, ?);''', a.db_data())
    conn.commit()


def export_database(us, path, password):
  """ Export a user's database with the specified password.

  :param us: the User who owns the database
  :param path: the path where the database gets exported
  :param password: the new password for the database
  """

  user_key = secrets.decrypt_field(us.crypt_key)
  new_key = secrets.derive_fernet_key(password)

  acc = accountdb.get_all_accounts(us)
  acc = [account.unpack(a) for a in acc]

  for a in acc:
    a.password = secrets.decrypt_data(user_key, a.password)
    a.password = secrets.encrypt_data(new_key, a.password)

  create_sharing_database(path)
  populate_sharing_database(path, acc)
  
    
def get_sharing_accounts(path):
  """ Return all acounts from a sharing database. """
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''SELECT * FROM accounts;''')
    return c.fetchall()


def import_database(us, path, password):
  """ Import a database for the specified user.

  The accounts which already exist in the user's database
  do not get replaced.

  :param us: the User who imports the database
  :param path: the path where the database is located
  :param password: the password with which the database was encrypted
  """

  # Create the user's database if it does not exist.
  accountdb.create_database(us)
  
  user_key = secrets.decrypt_field(us.crypt_key)
  old_key = secrets.derive_fernet_key(password)

  acc = get_sharing_accounts(path)  
  acc = [account.unpack(a) for a in acc]

  for a in acc:
    a.password = secrets.decrypt_data(old_key, a.password)
    a.password = secrets.encrypt_data(user_key, a.password)
    try:
      accountdb.insert_account(us, a)
    except accountdb.AccountExistsException:
      pass
      
