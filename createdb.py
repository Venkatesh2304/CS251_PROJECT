import psycopg2

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS msg_server""")
cur.execute("""CREATE TABLE msg_server(
             OID INTEGER,
             SENDER TEXT,
             RECIEVER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             PRIMARY KEY(SENDER,OID));""")
cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_server(RECIEVER)")
conn.commit()
conn.close()

