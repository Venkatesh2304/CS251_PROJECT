import psycopg2

conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")

cur = conn.cursor()

# cur.execute("""DROP TABLE IF EXISTS Users""")
# cur.execute("""CREATE TABLE Users(
#              USERNAME TEXT PRIMARY KEY,
#              PASSWORD TEXT,
#              STATUS TEXT,
#              PORT INTEGER);""")

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

# cur.execute("""DROP TABLE IF EXISTS msg_client_sent""")
# cur.execute("""CREATE TABLE msg_client_sent(
#              ID INTEGER PRIMARY KEY,
#              RECIEVER TEXT,
#              MESSAGE TEXT,
#              TYPE TEXT,
#              TIME_SENT TIMESTAMP,
#              TIME_RECIEVED TIMESTAMP);""")
# cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_client_sent(RECIEVER)")

# cur.execute("""DROP TABLE IF EXISTS msg_client_recieved""")
# cur.execute("""CREATE TABLE msg_client_recieved(
#              ID INTEGER PRIMARY KEY,
#              SENDER TEXT,
#              MESSAGE TEXT,
#              TYPE TEXT,
#              TIME_SENT TIMESTAMP,
#              TIME_RECIEVED TIMESTAMP);""")
# cur.execute("CREATE INDEX SENDER_INDEX ON msg_client_recieved(SENDER)")

# cur.execute("""DROP TABLE IF EXISTS Groups""")
# cur.execute("""CREATE TABLE Gropus(
#              ID INTEGER PRIMARY KEY,
#              NAME TEXT,
#              ADMIN TEXT,
#              MEMBERS TEXT);""")

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
# cur.execute("CREATE INDEX RECIEVER_INDEX ON msg_grp_server()")

conn.commit()
conn.close()

