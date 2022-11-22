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
             TIME_RECIEVED TIMESTAMP,
             PRIMARY KEY(SENDER,OID));""")
cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_server(RECIEVER)")

cur.execute("""DROP TABLE IF EXISTS msg_client_sent""")
cur.execute("""CREATE TABLE msg_client_sent(
             ID INTEGER IDENTITY PRIMARY KEY,
             RECIEVER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             TIME_RECIEVED TIMESTAMP);""")
cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_client_sent(RECIEVER)")

cur.execute("""DROP TABLE IF EXISTS msg_client_recieved""")
cur.execute("""CREATE TABLE msg_client_sent(
             ID INTEGER IDENTITY PRIMARY KEY,
             SENDER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             TIME_RECIEVED TIMESTAMP);""")
cur.execute("CREATE INDEX SENDER_INDEX ON msg_client_reciever(SENDER)")

conn.commit()
conn.close()

