from connectdb import connectToDB 
conn = connectToDB()

def addMessage(sender,message,typ):
    cur = conn.cursor()
    cur.execute("SELECT * FROM msg_client_recieved")
    id = len(cur.fetchall()) + 1
    cur.execute(f"""INSERT INTO msg_client_recieved(ID, SENDER,MESSAGE,TYPE) VALUES ({id},'{sender}','{message}','{typ}')""")
    conn.commit()
    


def updateTimeSent(id,timeSent):
    cur = conn.cursor()
    cur.execute(f"""UPDATE msg_client_sent SET TIME_RECIEVED = TIMESTAMP '{timeSent}' WHERE ID = '{id}' """)
    conn.commit()

def updateTimeRecieved(id,timeRecieved):
    cur = conn.cursor()
    cur.execute(f"""UPDATE msg_client_recieved SET TIMESENT = TIMESTAMP '{timeRecieved}' WHERE ID = '{id}' """)
    conn.commit()