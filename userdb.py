import sqlite3

DB_PATH = 'users.db'

def create_database():
  with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (name text, password text, crypt_key text);''')


def get_users_by_name(cursor, name):
  query_string = '%' + name + '%'
  cursor.execute('SELECT * FROM users WHERE name LIKE ?;', (query_string,))
  return cursor.fetchall()


def insert_user(cursor, user):
  present = get_users_by_name(cursor, user.name)
  if len(present) > 0:
    # TODO: Find a better exception to raise.
    raise Exception
  cursor.execute('INSERT INTO users VALUES(?,?,?);', user.db_data())


def delete_user(cursor, user):
  cursor.execute('''DELETE FROM users
                    WHERE name=? AND password=?
                    AND crypt_key=?;''', user.db_data())
