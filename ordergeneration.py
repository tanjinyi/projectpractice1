import sqlite3 as lite
import sys

con = lite.connect('orders.db')

with con:
	cur = con.cursor()	
	cur.execute("DROP TABLE IF EXISTS merch")
	cur.execute("CREATE TABLE orders(email TEXT, pid INT, quantity INT, order_date TEXT)")
