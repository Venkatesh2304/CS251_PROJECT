# function to add sent msg with other attributes 
# function to add read_reciept or read_Reciepts id and recieved time from server ( id also comes )
# same as above from client 
# function to get offline messages 
# function to add recieved msg or msgs with recieved time 
from connectdb import connectToDB 
conn = connectToDB()

def addMessage(reciever,message,typ):
    cur = conn.cursor()
    cur.execute("SELECT * FROM msg_client_sent")
    id = len(cur.fetchall()) + 1
    cur.execute(f"""INSERT INTO msg_client_sent(ID, RECIEVER,MESSAGE,TYPE) VALUES ({id},'{reciever}','{message}','{typ}')""")
    conn.commit() 
    return id 


def updateTimeSent(id,timeSent):
    cur = conn.cursor()
    cur.execute(f"""UPDATE msg_client_sent SET TIME_SENT = TIMESTAMP '{timeSent}' WHERE ID = '{id}' """)
    conn.commit()

def updateTimeRecieved(id,timeRecieved):
    cur = conn.cursor()
    cur.execute(f"""UPDATE msg_client_sent SET TIME_SENT = TIMESTAMP '{timeRecieved}' WHERE ID = '{id}' """)
    conn.commit()

