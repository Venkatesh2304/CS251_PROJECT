from datetime import datetime
from connectdb import connectToDB 
conn = connectToDB()

#adds a message sent to database
#checks for _id collision 
#return the new id even if already inserted 
def addMessage(oid,sender,reciever,message,typ,timesent):
    #remove timeseen , add old _id (_id) while adding check wheter the old _id for that sender is already there 
    cur = conn.cursor()
    # cur.execute(f"""INSERT INTO msg_server(OID,SENDER,RECIEVER,MESSAGE,TYPE,TIME_SENT) VALUES ({oid},'{sender}','{reciever}','{message}','{typ}', TIMESTAMP '{timesent}')""")
    # conn.commit()
    try:
        timesent = datetime.fromtimestamp(timesent)
        cur.execute(f"""INSERT INTO msg_server(OID,SENDER,RECIEVER,MESSAGE,TYPE,TIME_SENT) VALUES ({oid},'{sender}','{reciever}','{message}','{typ}', TIMESTAMP '{timesent}')""")
        conn.commit()
    except:
        return

#gives all the unrecieved messages of a user
#rtype [[]] 
def getAllUnrecievedMsg(user):
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM msg_server WHERE RECIEVER='{user}'""")
    msg_list = cur.fetchall()
    return msg_list

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

#function to update the id, recieved time  ,receiver (verify)
#delete msg [id] 
  












# #updates the status of messages recieved by user
# def updateRecievedStatus(user):
#     cur=conn.cursor()
#     cur.execute(f"""UPDATE msg_server SET STATUS='R' WHERE RECIEVER='{user}' AND STATUS='NR'""")
#     conn.commit()

#STATUS = S/R/NR (seen,recieved,not recieved)
#give time as datetime.datetime.now(timezone.utc)
#gives all unread but recieved messages from a contact of a user 
# def getUnreadtMsg(user,contact):
#     cur = conn.cursor()
#     cur.execute(f"""SELECT ID,MESSAGE,TYPE,STATUS,TIME_SENT,TIME_SEEN FROM msg_server WHERE RECIEVER='{user}' AND SENDER='{contact}' AND STATUS='R'""")
#     msg_list = cur.fetchall()
#     return msg_list

# #gives all unrecieved messages from a contact of a user 
# def getUnrecievedtMsg(user,contact):
#     cur = conn.cursor()
#     cur.execute(f"""SELECT ID,MESSAGE,TYPE,STATUS,TIME_SENT,TIME_SEEN FROM msg_server WHERE RECIEVER='{user}' AND SENDER='{contact}' AND STATUS='NR'""")
#     msg_list = cur.fetchall()
#     return msg_list 

#gives all seen messages from a contact of a user 
# def getReadtMsg(user,contact):
#     cur = conn.cursor()
#     cur.execute(f"""SELECT ID,MESSAGE,TYPE,STATUS,TIME_SENT,TIME_SEEN FROM msg_server WHERE RECIEVER='{user}' AND SENDER='{contact}' AND STATUS='S'""")
#     msg_list = cur.fetchall()
#     return msg_list

# removes messages seen from a contact of a user 
# def removeReadMessages(user,contact):
#     cur = conn.cursor()
#     cur.execute(f"""DELETE FROM msg_server WHERE RECIEVER='{user}' AND SENDER='{contact}' AND STATUS='S'""")
#     conn.commit()
#updates the status of messages seen by user
# def updateSeenStatus(user,contact,time_seen):
#     cur=conn.cursor()
#     cur.execute(f"""UPDATE msg_server SET STATUS='S', TIME_SEEN = TIMESTAMP '{time_seen}' WHERE RECIEVER='{user}' AND SENDER='{contact}'""")
#     conn.commit()
