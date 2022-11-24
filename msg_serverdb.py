from datetime import datetime
import time
from connectdb import connectToDB 
conn = connectToDB()

#adds a message sent to database
#checks for _id collision 
#return the new id even if already inserted 
def addMessage(oid,sender,reciever,message,typ,isGroup):
    cur = conn.cursor()
    cur.execute("SELECT * FROM msg_server")
    timesent = datetime.fromtimestamp(timesent)
    try:
       if isGroup : 
          cur.execute(f"SELECT MEMBERS FROM Groups WHERE NAME = '{reciever}' ")
          m = cur.fetchone()[0]
          #print("All group members : ",m )
          m = m.split(",")
          m.remove(sender)
          m = ",".join(m)
          print("Filtered members :: ", m )
          cur.execute(f"""INSERT INTO msg_grp_server(GNAME,MID,SENDER,MESSAGE,TYPE,COUNT,NOTSEEN) VALUES ('{reciever}',{oid},'{sender}','{message}','{typ}',1,'{m}')""")
       else : 
          cur.execute(f"""INSERT INTO msg_server(OID,SENDER,RECIEVER,MESSAGE,TYPE) VALUES ({oid},'{sender}','{reciever}','{message}','{typ}')""")
       conn.commit()
    except Exception as e : 
        print(e,2)

#gives all the unrecieved messages of a user
#rtype [[]] 
def getAllUnrecievedMsg(user):
    cur = conn.cursor()
    cur.execute("SELECT * FROM msg_server")
    cur.execute(f"""SELECT * FROM msg_server WHERE RECIEVER='{user}'""")
    data = [{ "sender" : msg[1] , "msg" : msg[3] , "id" : msg[0]  , "sent" : msg[5].timestamp() , "group" : False , "type" : msg[4]  } for msg in cur.fetchall() ]
    cur.execute(f"""SELECT * FROM msg_grp_server WHERE NOTSEEN LIKE '%{user}%'""")
    data += [{ "sender" : msg[2] , "group" : msg[0] ,  "id" : msg[1] , "msg" : msg[3] , "sent" : msg[5].timestamp() , "type" : msg[4] } for msg in cur.fetchall() ]
    return data 

def getAllReadRecipts(sender):
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM msg_server WHERE SENDER='{sender}' AND TIME_RECIEVED IS NOT NULL""")
    data = [{ "level":2, "id" : msg[0]  , "time" : msg[6].timestamp()} for msg in cur.fetchall() ]
    return data

#removes the message with the given id, useless ig
#id ,reciever 
#[id] , reciever
def removeMessage(id,sender,reciever):
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM msg_server WHERE OID = {id} AND SENDER = '{sender}' AND RECIEVER = '{reciever}'""")
    conn.commit()

def updateTimeRecieved(oid, sender, reciever, timeRecieved):
    cur = conn.cursor()
    timeRecieved = datetime.fromtimestamp(timeRecieved)
    cur.execute(f"""UPDATE msg_server SET TIME_RECIEVED = TIMESTAMP '{timeRecieved}' WHERE OID = '{oid}' AND SENDER = '{sender}' AND RECIEVER = '{reciever}'  """)
    conn.commit()

def updateTimeSent(oid, sender, reciever, timeSent):
    cur = conn.cursor()
    timeSent = datetime.fromtimestamp(timeSent)
    cur.execute(f"""UPDATE msg_server SET TIME_SENT = TIMESTAMP '{timeSent}' WHERE OID = '{oid}' AND SENDER = '{sender}' AND RECIEVER = '{reciever}'  """)
    conn.commit()

def updateCount(mid,sender,reciever):
    cur = conn.cursor()
    cur.execute(f"""SELECT COUNT,NOTSEEN FROM msg_grp_server WHERE MID = {mid} AND SENDER = '{sender}'""")
    (count,notseen) = cur.fetchone()
    count += 1 
    notseen = notseen.split(",")
    notseen.remove(reciever)
    m = ",".join(notseen)
    cur.execute(f"""UPDATE msg_grp_server SET COUNT = {count}, NOTSEEN = '{m}'""")
    if (count == max):
        cur.execute(f"""DELETE FROM msg_grp_server WHERE MID = {mid} AND SENDER = '{sender}' """)

def createGroup(admin,name):
        cur = conn.cursor()  
        cur.execute("SELECT * FROM Groups")
        id = len(cur.fetchall())+1
        cur.execute(f"SELECT ID FROM Groups WHERE NAME = '{name}'")
        x = cur.fetchall()
        if x : 
           return 1   
        cur.execute(f"""INSERT INTO Groups(ID,NAME,ADMIN,MEMBERS) VALUES ({id},'{name}','{admin}','{admin}')""")
        conn.commit()
        cur.execute("SELECT * FROM Groups")
        return id

def addMembers(admin,gname,members):
    cur = conn.cursor()
    if (type(members) != list ):
        members = [members]
    cur.execute(f"SELECT MEMBERS FROM Groups WHERE NAME='{gname}' AND ADMIN = '{admin}'")
    m = cur.fetchone()[0]
    for i in members:
        if (i not in m):
            m = m+","+i
    cur.execute(f"UPDATE Groups SET MEMBERS = '{m}' WHERE NAME='{gname}' AND ADMIN = '{admin}'")
    conn.commit()

def getAllGroupMembers(gname):
    cur = conn.cursor()
    cur.execute(f"SELECT MEMBERS FROM Groups WHERE NAME = '{gname}' ")
    return cur.fetchone()[0]

def addPublicKey(user, key):
    cur = conn.cursor()
    cur.execute(f"""UPDATE Users SET PUBLIC_KEY = '{key}' WHERE USERNAME = '{user}'""")
    conn.commit()

def getPublicKey(user):
        cur = conn.cursor()
        #time.sleep(1)
        
        cur.execute(f"""SELECT PUBLIC_KEY FROM Users WHERE USERNAME = '{user}'""")
        x = cur.fetchone()
        #print(user,x)
        return int(x[0])

