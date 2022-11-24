import json
import threading
import socket
import time 
from Socket import Socket
import pandas as pd 
import msg_serverdb as msg_db
import userdb  as user_db 

#for user in ["venkatesh","aadithya","atishay","yash"] : 
#    user_db.signUpUser(user,"123")

clients = {}

# class DB(pd.DataFrame) :
#       def  __init__(self) : 
#           super().__init__([],columns = ["id","_id","sender","reciever","msg","sent","recieved"])
#       def add_msg(self,_id,sender,reciever,msg,time) :
#           id = 1 if len(self.index) == 0 else self.index[-1] + 2 
#           self.loc[len(self)] = [id,_id,sender,reciever,msg,time,None]
#           return int(id) 
#       def delete_msg(self,id) : 
#           self = self[self.id != id ]
#       def update_recieve_time(self,id,time) : 
#           self.loc[self.id == id, 'recieved'] = time 
#       def get_sender(self,id) :
#           return self[self.id == id]["sender"].iloc[0]
#       def get_unread_msg(self,reciever) :
#           return self[(self.reciever == reciever) & (self.recieved.isna()) ].to_dict(orient="records")
#       def get_read_reciept(self,sender) : 
#           return self[(self.sender == sender) & (self.recieved.notna()) ].to_dict(orient="records")

def client_handle(conn,addr) : 
    connection = ClientConnection(conn,addr)
    connection.start()

# Create a TCP/IP socket
class ClientConnection(Socket) : 
      
      def __init__(self, _socket , addr = None ):
          self.addr = addr  
          super().__init__(_socket)
          self.preauth_url_maps = {"/signup" : self.signup , "/login" : self.login }
          self.url_maps = { "/test" : self.test , "/send_msg"  : self.send_msg , "/read_reciept" : self.read_reciept , 
                            "/create_group" : self.create_group , "/add_members" : self.add_members }
          is_group_creating = False 

      def login(self,data,headers) :
          isLogged = user_db.logInUser(data["user"],data["password"],self.addr[1]) 
          if isLogged :
            self.is_authorised = True 
          self.user = data['user']
          clients[self.user] = self  
          self.add_send_queue("/login_res", isLogged)
          thread = threading.Thread(target = self.intial_send )
          thread.start()
          return isLogged
          
      def signup(self,data,headers):
          isCreated = user_db.signUpUser(data["user"],data["password"])
          if isCreated : 
             self.login(data,headers)
          self.add_send_queue("/signup_res", isCreated)

      def get_public_key(self,user,headers) :
          self.add_send_queue("/public_key_response",json.dumps(self.db.get_public_key(user)))
      
      def send_key(self,data,headers) : 
          clients[data["to"]].add_send_queue("/set_secret_key",data)

      def send_msg(self,data,headers) :
          id , to , isGroup  = data["id"] , data["to"] , data["group"] 
          t =  time.time()
          msg_db.addMessage(id,self.user,data["to"],data["msg"],data["type"],t,isGroup)
          self.add_send_queue("/read_reciept", {"time" : t  , "id" : id , "level" : 1 })
          if isGroup : 
              recievers = msg_db.getAllGroupMembers(to).split(",")
              recievers.remove(self.user)
          else : 
             recievers = [to]
          for reciever in recievers : 
            if reciever in clients :  #to be replaced 
               new_data = { "sender" : self.user , "msg" : data["msg"] , "id" : id  , "sent" : t , "group" : data["group"] ,
                             "type" : data["type"]  }
               clients[reciever].add_send_queue("/recieve_msg",new_data)
      
      def read_reciept(self,data,headers) :
          id , sender  = data["id"] , data["sender"]
          if data["group"] : 
             msg_db.updateCount(id,sender,self.user)
          else : 
            msg_db.updateTimeRecieved(id,sender,self.user,data["time"])
            if sender in clients :
               clients[sender].add_send_queue("/read_reciept", {"time" : data["time"] , "id" : id , "level" :2 },
                                                  {}, lambda : msg_db.removeMessage(id,sender,self.user) )
              
      def intial_send(self) : 
          unread_msgs = msg_db.getAllUnrecievedMsg(self.user)
          unread_read_reciepts = msg_db.getAllReadRecipts(self.user)
          for msg in unread_msgs :
             self.add_send_queue("/recieve_msg", msg)
          for msg in unread_read_reciepts :
             self.add_send_queue("/read_reciept", msg)
          
      def test(self,data,headers) : 
          if data.count("test messsage number") != 1000 : 
              raise Exception("full not recieved" + data[:10])
          print('received {!r}'.format(data.replace("test messsage number","")) + " :: " + str(self.addr[1]) + " :: " + str(headers) ) 
      
      def create_group(self,data,headers) : 
          msg_db.createGroup(self.user,data["gname"])
          self.add_send_queue("/ack",'"creategroup"')

      def add_members(self,data,headers) : 
          msg_db.addMembers(self.user,data["gname"],data["members"])
          self.add_send_queue("/ack","'add_member'")

         
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server_address = ('localhost', 10000)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(100)

while True:
        connection, client_address = sock.accept()
        print('Connection from', client_address)
        client_thread = threading.Thread(target=client_handle,args=(connection,client_address))
        client_thread.start()
        