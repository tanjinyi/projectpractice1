import sqlite3 as lite
import sys

merchandise = {
    ('A4 lecture pad', 2.60),
    ('7-colour sticky not with pen', 4.20),
    ('A5 ring book', 4.80),
    ('A5 note book with zip bag', 4.60),
    ('2B pencil', 0.90),
    ('Stainless steel tumbler', 12.90),
    ('A4 clear holder', 4.40),
    ('A4 vanguard file', 1.00),
    ('Name card holder', 10.90),
    ('Umbrella', 9.00),
    ('School badge (Junior High)', 1.30),
    ('School badge (Senior High)', 1.80),
    ('Dunman dolls (pair)', 45.00)
}

con = lite.connect('merchandise.db')

with con:
	cur = con.cursor()	
	cur.execute("DROP TABLE IF EXISTS merch")
	cur.execute("CREATE TABLE merch(pid INTEGER PRIMARY KEY AUTOINCREMENT, merchandise TEXT, price MONEY)")
	cur.executemany("INSERT INTO merch(merchandise,price) VALUES(?,?)", merchandise)

con.close()
