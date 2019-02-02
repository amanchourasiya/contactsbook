import sqlite3

conn = sqlite3.connect('contacts.db')
conn.execute('delete from contacts where name=?',('wpwpwpwp',))
conn.commit()

