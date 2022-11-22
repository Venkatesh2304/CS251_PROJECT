import socket
import sys
import time 
import json 
import http.client
import threading
from Socket import Socket 
import msg_client as db 
#env variables
server_address = ('localhost', 10000 )

# class DB() : 
#       _msg = []
#       msg = {}
#       def add_msg(self,to,msg) :
#           _id = len(self._msg) 
#           self._msg.append(msg)
#           return _id 

class Client(Socket) : 
      def __init__(self, _socket , user , addr = None ):
          self.addr = addr    
          self.user =  user
          self.db = db
          super().__init__(_socket)
          self.url_maps = { "/login_res" : self.login_res , "/signup_res" : self.signup_res , 
                            "/read_reciept" : self.read_reciept , "/recieve_msg": self.recieve_msg}
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
          id = self.db.add_sent_msg(to,msg)
          msg = {  "id": id  , "to" : to , "msg" : msg }
          self.add_send_queue("/send_msg",msg,headers)
      def recieve_msg(self,data,headers) : 
          t = time.time()
          if type(data) == list : 
             for data in data : 
                self.print(f"""Message recv from :: {data['sender']}  , id ::  {data['id']} ,time :: {data['sent']} {data['msg']}  """)
                self.add_send_queue("/read_reciept", {"id": data['id'] , "time": t})
                self.db.add_recv_msg( data["id"] , data["sent"] , data["msg"] , t )
          else : 
             self.print(f"""Message  recv from  :: {data['sender']}  , time :: {data['sent']} , id :: {data['id']} ,  {data['msg']} """)
             self.db.add_recv_msg( data["id"] , data["sent"] , data["msg"] , t )
             self.add_send_queue("/read_reciept", {"id": data['id'] , "time": t})
             
      def read_reciept(self,data,headers) : 
          level = data["level"]
          if level == 0 : 
             self.print(f"Error Sending to Server :: {self.db._msg[data['id']]} ")
          else :
            msg = self.db.get_msg_id(data["id"])
            if level == 1 :     
              self.db.update_time_sent( data["id"] , data["time"] )
              self.print(f"Message Sent to Server :: {msg} {data['time']}") 
            elif level == 2  : 
               if "reciepts" in data : 
                 for data in data["reciepts"] : 
                   self.print(f"Message Sent to Reciever :: {msg} {data['time']} ")                    
               else : 
                   self.print(f"Message Sent to Reciever :: {msg} {data['time']} ")
                   self.db.update_recv_time(data["id"],data["time"])                    
            else : 
                pass 
      def print(self,*args) : 
          #args = (f"Client {self.user} ",) + args  
          print(*args)          
        
sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) , 1)
sock.connect(server_address)
sock.start()
sock.login_req(input("user : "),input("pass : "))
while True : 
     sock.send_msg(input("send to : "),input("msg : "))   



# n = 2
           
# def t(k) : 
#  sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) , k)
#  sock.connect(server_address)
#  sock.start()
#  print(f"client {k} started")
#  if len(sys.argv) == 2 : 
#      sock.login_req(input("user : "),input("pass : "))
#      input()
#  else :
#    sock.login_req(str(k),"1")

#  for i in range(2) :
#      msg = "test messsage number"  +  f" client ==> {k} msg_no ==> {i}"
#      sock.send_msg(str(n-k),msg)   
#      time.sleep(1)
#  #time.sleep(100)

# #t(1)

# for i in range(1,n) : 
#          client_thread = threading.Thread(target=t,args=(i,))
#          client_thread.start()



