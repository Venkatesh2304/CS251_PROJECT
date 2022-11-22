import os
import sys  
import time 
import threading
import random
print(1)
clients = ["venkatesh","aadithya","atishay","yash"]
msg_to = ["venkatesh","aadithya","atishay","yash"]
msg_to.reverse()
def p(i) : 
    os.system(f"python ../client.py < in_{clients[i]} ")
os.system("rm out_* && rm in*")

y = threading.Thread( target= lambda : os.system(f"python ../server.py") , daemon=True)
y.start()
time.sleep(1)
for i in range(0,len(clients)) :
    with open(f"in_{clients[i]}","w+") as f : 
        f.write("\n".join([clients[i],"123" ,msg_to[i],str(random.randint(0,100)),"-1","\n"]))
    x = threading.Thread( target= p , args=(i,) , daemon=True )
    x.start()
    time.sleep(1)
os.system("tail " + " ".join([ "out_" + i for i in clients ]) + " > output.txt")
os.system("tail " + " ".join([ "in_" + i for i in clients ]) + " > input.txt")
time.sleep(1)
# y.terminate()