import psycopg2

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()

conn.commit()
conn.close()

