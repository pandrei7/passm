import sqlite3

import account
import accountdb
import secrets
import user

def create_sharing_database(path):
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS accounts;''')
    c.execute('''CREATE TABLE accounts
                 (name text, email text, username text, password text);''')


def populate_sharing_database(path, acc):
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    for a in acc:
      c.execute('''INSERT INTO accounts VALUES (?, ?, ?, ?);''', a.db_data())
    conn.commit()


def export_database(us, path, password):
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
  with sqlite3.connect(path) as conn:
    c = conn.cursor()
    c.execute('''SELECT * FROM accounts;''')
    return c.fetchall()


def import_database(us, path, password):
  # Create the user database if it does not exist
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
      
