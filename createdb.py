import psycopg2
from psycopg2.extras import LoggingConnection
import logging 

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()

cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
rows = cur.fetchall()
for row in rows:
    cur.execute("drop table " + row[1] + " cascade")
conn.commit()


cur.execute("""DROP TABLE IF EXISTS Users""")
cur.execute("""CREATE TABLE Users(
             USERNAME TEXT PRIMARY KEY,
             PASSWORD TEXT,
             STATUS TEXT,
             PORT INTEGER,
             PUBLIC_KEY TEXT);""")


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
# cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_server(RECIEVER)")
    
cur.execute("""DROP TABLE IF EXISTS msg_client_sent""")
cur.execute("""CREATE TABLE msg_client_sent(
             ID INTEGER PRIMARY KEY,
             ISGROUP TEXT,
             RECIEVER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             TIME_RECIEVED TIMESTAMP);""")
             
cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_client_sent(RECIEVER)")

cur.execute("""DROP TABLE IF EXISTS msg_client_recieved""")
cur.execute("""CREATE TABLE msg_client_recieved(
             ID INTEGER PRIMARY KEY,
             ISGROUP TEXT,
             SENDER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             TIME_RECIEVED TIMESTAMP);""")

# cur.execute("CREATE INDEX SENDER_INDEX ON msg_client_recieved(SENDER)")

cur.execute("""DROP TABLE IF EXISTS Groups""")
cur.execute("""CREATE TABLE Groups(
             NAME TEXT PRIMARY KEY,
             ADMIN TEXT,
             MEMBERS TEXT);""")

cur.execute("""DROP TABLE IF EXISTS msg_grp_server""")
cur.execute("""CREATE TABLE msg_grp_server(
             GNAME TEXT,
             MID INTEGER,
             SENDER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             COUNT INTEGER,
             NOTSEEN TEXT,
             PRIMARY KEY(GNAME,MID));""")

cur.execute("""DROP TABLE IF EXISTS server_key_msg""")
cur.execute("""CREATE TABLE server_key_msg(
             SNEDER TEXT,
             TO TEXT,
             KEY TEXT,
             ISGROUP TEXT
             PRIMARY KEY(SENDER,TO));""")

# cur.execute("""CREATE TABLE keys_client(
#              CONTACT PRIMARY KEY,
#              KEY TEXT);""")

# cur.execute("""CREATE TABLE keys_server(
#              USER TEXT PRIMARY KEY ,
#              KEY TEXT);""")

# cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_grp_server()")

cur.execute("CREATE INDEX SENDER_INDEX ON msg_client_recieved(SENDER)")
conn.commit()
conn.close()


