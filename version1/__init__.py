import sqlite3

email="743869857@qq.com"
w=email,
conn = sqlite3.connect("D:/bot/actions/customer.db")
cursor = conn.cursor()
query1 = "CREATE TABLE IF NOT EXISTS customer (id integer PRIMARY KEY,email text NOT NULL, phone integer NOT NULL);"
cursor.execute(query1)
query = "SELECT * FROM customer where email = ?"
cursor.execute(query,w)
if not cursor.fetchall():
    print("cursor.fetchall()")

cursor.close()
conn.commit()
conn.close()