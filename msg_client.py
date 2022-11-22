# function to add sent msg with other attributes 
# function to add read_reciept or read_Reciepts id and recieved time from server ( id also comes )
# same as above from client 
# function to get offline messages 
# function to add recieved msg or msgs with recieved time 
from datetime import datetime
from connectdb import connectToDB 
conn = connectToDB()

def getMsgSent(id):
    cur = conn.cursor()
    cur.execute(f"SELECT MESSAGE FROM msg_client_sent WHERE ID = {id}")
    return cur.fetchone()[0]

def addSentMsg(reciever,message,typ,isgroup=False):
    cur = conn.cursor()
    cur.execute("SELECT * FROM msg_client_sent")
    id = len(cur.fetchall()) + 1
    if (isgroup):
        cur.execute(f"""INSERT INTO msg_client_sent(ID, RECIEVER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{reciever}','{message}','{typ}','TRUE')""")
    else :
        cur.execute(f"""INSERT INTO msg_client_sent(ID, RECIEVER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{reciever}','{message}','{typ}','FALSE')""")
    conn.commit() 
    return id 

def updateTimeSent(id,timeSent):
    cur = conn.cursor()
    timeSent = datetime.fromtimestamp(timeSent)
    cur.execute(f"""UPDATE msg_client_sent SET TIME_SENT = TIMESTAMP '{timeSent}' WHERE ID = '{id}' """)
    conn.commit()

def updateTimeRecieved(id,timeRecieved):
    cur = conn.cursor()
    timeRecieved = datetime.fromtimestamp(timeRecieved)
    cur.execute(f"""UPDATE msg_client_sent SET TIME_SENT = TIMESTAMP '{timeRecieved}' WHERE ID = '{id}' """)
    conn.commit()

def addRecvMsg(id,sender,message,timeSent,typ,isgroup=False):
    cur = conn.cursor()
    cur.execute("SELECT * FROM msg_client_recieved")
    timeSent = datetime.fromtimestamp(timeSent)
    if (isgroup):
            cur.execute(f"""INSERT INTO msg_client_recieved(ID, SENDER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{sender}','{message}','{typ}','TRUE')""")  
    else:
            cur.execute(f"""INSERT INTO msg_client_recieved(ID, SENDER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{sender}','{message}','{typ}','FALSE')""")
    conn.commit()
