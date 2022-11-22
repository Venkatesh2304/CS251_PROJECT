import os  
import time 
import threading

clients = ["ven","aad"]
msg_to =  ["aad","ven"]
def p(i) : 
    os.system(f"python ../client.py < in_{clients[i]} > out_{clients[i]}")

x = threading.Thread( target= lambda : os.system(f"python ../server.py") )
x.start()
time.sleep(1)
for i in range(0,len(clients)) :
    with open(f"in_{clients[i]}","w+") as f : 
        f.write("\n".join([clients[i],"123",msg_to[i],str(i),"-1","\n"]))
    x = threading.Thread( target= p , args=(i,)  )
    x.start()
    time.sleep(3)