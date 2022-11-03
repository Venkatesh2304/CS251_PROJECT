from msg_serverdb import *
from datetime import datetime,timezone
import time

# for i in range (0,100):
#     dt = datetime.now(timezone.utc)
#     addMessage(i,f"user{i}",f"user{i%10}",f"Hi {i%10}","str",dt,dt)

#updateSeenStatus("user2","user42",datetime.now(timezone.utc))
#removeReadMessages("user2","user42")
for i in getReadtMsg("user2","user42"):
    print(i)


# for i in getUnreadtMsg("user2","user22",datetime.now(timezone.utc)):
#     print(i)

#removeUnreadMessages("user2","user22")