import psycopg2

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS test""")
cur.execute("""CREATE TABLE test(
             id INT SERIAL PRIMARY KEY,
             NAME TEXT);""")
cur.execute("""INSERT INTO test(NAME) VALUES('abc')""")
cur.execute("""INSERT INTO test(NAME) VALUES('def')""")
cur.execute("""INSERT INTO test(NAME) VALUES('ghi')""")

cur.execute("SELECT * FROM test")
for i in cur.fetchall():
    print(i)