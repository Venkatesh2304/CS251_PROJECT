import socket
import sys
import time 
import json 
import http.client
import threading
from Socket import Socket 

#env variables
server_address = ('localhost', 10000 )
class DB() : 
      _msg = []
      def add_msg(self,to,msg) :
          _id = len(self._msg) 
          self._msg.append(to + " ==> " + msg)
          return _id 
      
class Client(Socket) : 
      def __init__(self, _socket , addr = None ):
          self.addr = addr    
          self.db = DB()
          super().__init__(_socket)
          self.url_maps = { "/login_res" : self.login_res , "/signup_res" : self.signup_res }
          self.preauth_url_maps = self.url_maps
    
      def login_req(self,user,password) :
          self.add_send_queue("/login",{"user" : user , "password" : password})
      def login_res(self,data,headers) : 
          if data : 
            print("You are logged in")
          else : 
            print("Credientials is wrong")
  
      def signup_req(self,user,password) : 
          self.add_send_queue("/signup",{"user" : user , "password" : password})
      def signup_res(self,data,headers) : 
          if data :
             print("User created") 
          else : 
             print("Already exists")
      
      def send_msg(self,to,msg,headers ={}) :
          _id  = self.db.add_msg(to,msg)
          msg = {  "id": _id  , "to" : to , "msg" : msg }
          self.add_send_queue("/send_msg",msg,headers)
        
      def read_reciept(self,data,headers) : 
          msg = self.db._msg[data["id"]]
          level = data["level"]
          if level == 0 : 
             print(f"Error Sending to Server :: {msg} ") 
          elif  level == 1 :     
             print(f"Message Sent to Server :: {msg} {data['time']}") 
          elif level == 2 : 
             print(f"Message Sent to Client :: {msg} {data['time']} ") 
          elif level == 3 : 
             print(f"Message Seen to Client :: {msg} {data['time']} ") 
          else : 
             print("Reciept Failure")
             
          



             
           
def t(k) : 
 sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) )
 sock.connect(server_address)
 sock.start()
 print(f"client {k} started")
 #sock.login_req(input("user : "),input("pass : "))
 sock.login_req("ven","12"+ str(k)[0])

 for i in range(10) :
     msg = "test messsage number"*1000 +  f":: client ==> {k} ,  msg_no ==> {i}"
     sock.add_send_queue("/test" , msg)    
     time.sleep(0.1)
 #time.sleep(100)

t(1)

# for i in range(100) : 
#         client_thread = threading.Thread(target=t,args=(i,))
#         client_thread.start()



