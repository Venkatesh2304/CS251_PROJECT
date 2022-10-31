import socket
import sys
import time 
import json 
import threading
from Socket import Socket 
class Client(Socket) : 
      pass 

def t(k) : 
 sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) )
 server_address = ('localhost', 10000 )
 sock.connect(server_address)
 print(f"client {k} started")
 for i in range(10) :
    msg = "test messsage number"*1000 +  f":: client ==> {k} ,  msg_no ==> {i}"
    sock.Send(msg.encode())    
    time.sleep(0.1)
 time.sleep(100)

for i in range(1,10) : 
        client_thread = threading.Thread(target=t,args=(i,))
        client_thread.start()



