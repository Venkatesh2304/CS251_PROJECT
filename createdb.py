import psycopg2

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Users;")
cur.execute("""CREATE TABLE Users(
             USERNAME TEXT PRIMARY KEY,
             PASSWORD TEXT,
             STATUS TEXT,
             PORT INT);""")
conn.commit()
conn.close()

