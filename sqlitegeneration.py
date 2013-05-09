import sqlite3 as lite
import sys

merchandise = {
    (1, 'A4 lecture pad', 2.60),
    (2,'7-colour sticky not with pen', 4.20),
    (3,'A5 ring book', 4.80),
    (4,'A5 note book with zip bag', 4.60),
    (5,'2B pencil', 0.90),
    (6,'Stainless steel tumbler', 12.90),
    (7,'A4 clear holder', 4.40),
    (8,'A4 vanguard file', 1.00),
    (9,'Name card holder', 10.90),
    (10,'Umbrella', 9.00),
    (11,'School badge (Junior High)', 1.30),
    (12,'School badge (Senior High)', 1.80),
    (13,'Dunman dolls (pair)', 45.00)
}

con = lite.connect('DATABASE.db')

with con:
	cur = con.cursor()	
	cur.execute("DROP TABLE IF EXISTS merch")
	cur.execute("CREATE TABLE merch(pid INTEGER, merchandise TEXT, price MONEY)")
	cur.execute("CREATE TABLE users(username TEXT, password TEXT, email TEXT, address TEXT)")
	cur.execute("INSERT INTO users VALUES ('admin', 'admin', 'admin@admin', 'admin')")
	cur.executemany("INSERT INTO merch(pid, merchandise,price) VALUES(?,?,?)", merchandise)
con.commit()
con.close()
