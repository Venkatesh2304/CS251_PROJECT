import socket
import sys
import time 
import json 
import threading
from Socket import Socket 
#env variables
server_address = ('localhost', 10000 )

class Client(Socket) : 
      def __init__(self, _socket , addr = None ):
          self.addr = addr  
          self.msg_id = 0 
          self.msg_without_reciepts = [] 
          super().__init__(_socket)
          self.url_maps = {"reciept" : self.reciept}
      def send_msg(self,msg,headers ={}) :
          headers = { "id": self.msg_id }
          self.add_send_queue("/test",msg,headers)
          self.msg_id += 1
       
      def reciept(self,body,headers) :
          if body["msg_id"] == "" : 

      def Auth(self,*args) : 
          if not self.user : 
             (self.user , self.pwd) = args  
             self.Send("/login", {""}) 

def t(k) : 
 sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) )
 sock.connect(server_address)
 sock.start()
 print(f"client {k} started")
 for i in range(10) :
    msg = "test messsage number"*1000 +  f":: client ==> {k} ,  msg_no ==> {i}"
    sock.add_send_queue("/test" , msg)    
    time.sleep(0.1)
 time.sleep(100)

for i in range(1) : 
        client_thread = threading.Thread(target=t,args=(i,))
        client_thread.start()



