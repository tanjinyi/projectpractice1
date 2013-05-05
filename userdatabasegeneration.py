import sqlite3 as lite
import sys

con = lite.connect('userdatabase.db')

with con:
	cur = con.cursor()	
	cur.execute("DROP TABLE IF EXISTS users")
	cur.execute("CREATE TABLE users(username TEXT, password TEXT, email TEXT, address TEXT)")
