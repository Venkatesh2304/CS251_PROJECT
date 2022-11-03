import psycopg2

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS msg_server""")
cur.execute("""CREATE TABLE msg_server(
             ID INT PRIMARY KEY,
             SENDER TEXT,
             RECIEVER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             STATUS TEXT,
             TIME_SENT TIMESTAMP,
             TIME_SEEN TIMESTAMP);""")
conn.commit()
conn.close()

