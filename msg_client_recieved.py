from connectdb import connectToDB 
conn = connectToDB()

def addMessage(sender,message,typ):
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO msg_client_recieved(SENDER,MESSAGE,TYPE) VALUES ('{sender}','{message}','{typ}')""")
    conn.commit()
    cur.execute("SELECT * FROM msg_client_recieved")
    return len(cur.fetchall())


def updateTimeSent(id,timeSent):
    cur = conn.cursor()
    cur.execute(f"""UPDATE msg_client_sent SET TIME_RECIEVED = TIMESTAMP '{timeSent}' WHERE ID = '{id}' """)
    conn.commit()

def updateTimeRecieved(id,timeRecieved):
    cur = conn.cursor()
    cur.execute(f"""UPDATE msg_client_recieved SET TIMESENT = TIMESTAMP '{timeRecieved}' WHERE ID = '{id}' """)
    conn.commit()