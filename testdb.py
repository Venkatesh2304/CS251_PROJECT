from msg_serverdb import *
from datetime import datetime,timezone
import time

# for i in range (0,100):
#     dt = datetime.now(timezone.utc)
#     addMessage(i,f"user{i}",f"user{i%10}",f"Hi {i%10 -1}","str",dt)


#updateSeenStatus("user2","user42",datetime.now(timezone.utc))
#removeReadMessages("user2","user42")
# for i in getReadtMsg("user2","user42"):
#     print(i)

# removeMessage([[5,"user5"],[15,"user5"]])
l = getAllUnrecievedMsg("user5")
for i in l:
    print(i)

# dt = datetime.now(timezone.utc)
# updateTimeRecieved(15,"user15","user5",dt)


# for i in getUnreadtMsg("user2","user22",datetime.now(timezone.utc)):
#     print(i)

#removeUnreadMessages("user2","user22")