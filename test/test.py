import os
import sys  
import time 
import threading
import random
import msg_client
import rsa  
n = 10
m = 5
msg_count = 5

os.system("python ../createdb.py")
os.system(f"python ../create_users.py {n}")
print("Users Created")

for i in range(n) : 
    for j in range(n) : 
        if i <= j : 
           x , y = msg_client.clientDB(str(i+1)) , msg_client.clientDB(str(j+1))
           key = os.urandom(16)
           x.add_secret_key(str(j+1),key)
           if i!= j :
             y.add_secret_key(str(i+1),key)
           
server = threading.Thread( target=lambda : os.system(f"python ../super_server.py {n}"))
server.start()
clients = [str(i+1) for i in range(n)]
os.system("rm out_* && rm in*")

def p(i) : 
    os.system(f"python ../client.py < in_{clients[i]} ")

for i in range(0,len(clients)) :
    with open(f"in_{clients[i]}","w+") as f : 
        msgs = [ f"Send {random.randint(1,n)} {str(random.randint(0,100))}" for j in range(msg_count) ]
        f.write("\n".join(
            ["l",clients[i],"123"] + msgs + ["Exit","\n"]
        ))

cmds = [ f"python ../client.py<in_{i+1}" for i in range(n) ]
os.system( "&".join(cmds) )

