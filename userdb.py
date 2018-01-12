import sqlite3

class UserExistsException(Exception):
  def __init__(self, name):
    Exception.__init__(self, 'User with name "' + name + '" already exists')


DB_PATH = 'dbs/users.db'


def create_database():
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (name text, password text, crypt_key text);''')


def get_users_by_name_exact(name):
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE name LIKE ?;', (name,))
    return c.fetchall()


def get_users_by_name(name):
  query_string = '%' + name + '%'
  return get_users_by_name_exact(query_string)


def insert_user(user):
  present = get_users_by_name_exact(user.name)
  if len(present) > 0:
    raise UserExistsException(user.name)

  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES(?,?,?);', user.db_data())
    conn.commit()


def delete_user(user):
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''DELETE FROM users
                      WHERE name=? AND password=?
                      AND crypt_key=?;''', user.db_data())
    conn.commit()
