import os
import secrets
import sqlite3
import user

class UserExistsException(Exception):
  def __init__(self, name):
    Exception.__init__(self, 'User with name "' + name + '" already exists')


class UserNotFoundException(Exception):
  def __init__(self, name):
    Exception.__init__(self, 'User with name "' + name + '" not found')


DB_DIR = 'dbs'
DB_NAME = '.supercalifragilistic'
DB_PATH = DB_DIR + '/' + DB_NAME + '.db'


def create_database():
  os.makedirs(DB_DIR, exist_ok=True)
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (name text, password text, crypt_key text);''')


def get_users_by_name_exact(name):
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE name LIKE ?;', (name,))
    return c.fetchall()


def get_users_by_name(name):
  query_string = '%' + name + '%'
  return get_users_by_name_exact(query_string)


def insert_user(us):
  present = get_users_by_name_exact(us.name)
  if len(present) > 0:
    raise UserExistsException(us.name)

  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES(?,?,?);', us.db_data())
    conn.commit()


def delete_user(us):
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''DELETE FROM users
                 WHERE name=? AND password=?
                 AND crypt_key=?;''', us.db_data())
    conn.commit()


def password_check(name, password):
  us = get_users_by_name_exact(name)
  if len(us) <= 0:
    raise UserNotFoundException(name)

  us = user.unpack(us[0])
  return password == secrets.decrypt_field(us.password)

