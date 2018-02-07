import os
import sqlite3

import user

class AccountExistsException(Exception):
  def __init__(self, name):
    Exception.__init__(self, 'Account with name "' + name + '" already exists')


def get_db_path(us):
  return 'dbs/' + us.name + '.db'


def create_database(us):
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (name text, email text, username text, password text);''')


def delete_database(us):
  try:
    os.remove(get_db_path(us))
  except:
    pass


def get_accounts_by_name_exact(us, name):
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE name LIKE ?;', (name,))
    return c.fetchall()


def get_accounts_by_name(us, name):
  query_string = '%' + name + '%'
  return get_accounts_by_name_exact(us, query_string)


def get_all_accounts(us):
  return get_accounts_by_name(us, '')


def insert_account(us, acc):
  present = get_accounts_by_name(us, acc.name)
  if len(present) > 0:
    raise AccountExistsException(acc.name)

  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('INSERT INTO accounts VALUES(?,?,?,?);', acc.db_data())
    conn.commit()


def delete_account(us, acc):
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''DELETE FROM accounts
                 WHERE name=? AND email=?
                 AND username=? AND password=?;''', acc.db_data())
    conn.commit()


def update_account_data(us, acc):
  path = get_db_path(us)
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''UPDATE accounts
                 SET name=?, email=?, username=?, password=?
                 WHERE name=?''', (*acc.db_data(), acc.name))
    conn.commit()


def change_account(us, acc):
  if len(get_accounts_by_name_exact(us, acc.name)) <= 0:
    insert_account(us, acc)
  else:
    update_account_data(us, acc)

