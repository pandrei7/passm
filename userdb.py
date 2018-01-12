import sqlite3

DB_PATH = 'dbs/users.db'

def create_database():
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (name text, password text, crypt_key text);''')


def get_users_by_name(name):
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    query_string = '%' + name + '%'
    c.execute('SELECT * FROM users WHERE name LIKE ?;', (query_string,))
    return c.fetchall()


def insert_user(user):
  present = get_users_by_name(user.name)
  if len(present) > 0:
    # TODO: Find a better exception to raise.
    raise Exception

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
