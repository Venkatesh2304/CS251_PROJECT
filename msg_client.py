# function to add sent msg with other attributes 
# function to add read_reciept or read_Reciepts id and recieved time from server ( id also comes )
# same as above from client 
# function to get offline messages 
# function to add recieved msg or msgs with recieved time 
from datetime import datetime
from connectdb import connectToDB 
conn = connectToDB()

class clientDB:
    def __init__(self, username):
        self.user = username
        cur = conn.cursor()
        cur.execute(f"""DROP TABLE IF EXISTS msg_client_sent_{username}""")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS msg_client_sent_{username}(
             ID INTEGER PRIMARY KEY,
             ISGROUP TEXT,
             RECIEVER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             TIME_RECIEVED TIMESTAMP);""")
        cur.execute(f"""DROP TABLE IF EXISTS msg_client_recieved_{username}""")
        cur.execute(f"""CREATE TABLE  IF NOT EXISTS msg_client_recieved_{username}(
             ID INTEGER PRIMARY KEY,
             ISGROUP TEXT,
             SENDER TEXT,
             MESSAGE TEXT,
             TYPE TEXT,
             TIME_SENT TIMESTAMP,
             TIME_RECIEVED TIMESTAMP);""")
        conn.commit()

    def getMsgSent(self,id):
        cur = conn.cursor()
        cur.execute(f"SELECT TYPE,MESSAGE FROM msg_client_sent_{self.user} WHERE ID = {id}")
        return cur.fetchone()
        
    def addSentMsg(self,reciever,message,typ,isgroup=False):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM msg_client_sent_{self.user}")
        id = len(cur.fetchall()) + 1
        if (isgroup):
            cur.execute(f"""INSERT INTO msg_client_sent_{self.user}(ID, RECIEVER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{reciever}','{message}','{typ}','TRUE')""")
        else :
            cur.execute(f"""INSERT INTO msg_client_sent_{self.user}(ID, RECIEVER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{reciever}','{message}','{typ}','FALSE')""")
        conn.commit() 
        return id 

    def updateTimeSent(self,id,timeSent):
        cur = conn.cursor()
        timeSent = datetime.fromtimestamp(timeSent)
        cur.execute(f"""UPDATE msg_client_sent_{self.user} SET TIME_SENT = TIMESTAMP '{timeSent}' WHERE ID = '{id}' """)
        conn.commit()

    def updateTimeRecieved(self,id,timeRecieved):
        cur = conn.cursor()
        timeRecieved = datetime.fromtimestamp(timeRecieved)
        cur.execute(f"""UPDATE msg_client_sent_{self.user} SET TIME_SENT = TIMESTAMP '{timeRecieved}' WHERE ID = '{id}' """)
        conn.commit()

    def addRecvMsg(self,id,sender,message,timeSent,typ,isgroup=False):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM msg_client_recieved_{self.user}")
        timeSent = datetime.fromtimestamp(timeSent)
        if (isgroup):
                cur.execute(f"""INSERT INTO msg_client_recieved_{self.user}(ID, SENDER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{sender}','{message}','{typ}','TRUE')""")  
        else:
                cur.execute(f"""INSERT INTO msg_client_recieved_{self.user}(ID, SENDER,MESSAGE,TYPE,ISGROUP) VALUES ({id},'{sender}','{message}','{typ}','FALSE')""")
        conn.commit()
