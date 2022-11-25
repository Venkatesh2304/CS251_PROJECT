import threading
import socket
import time 
from Socket import Socket
import pandas as pd 
import msg_serverdb as msg_db
import userdb  as user_db 

def client_handle(conn,addr,clients) : 
    connection = ClientConnection(conn,addr,clients)
    connection.start()

# Create a TCP/IP socket
class ClientConnection(Socket) : 
      
      def __init__(self, _socket , addr , clients  ):
          self.addr = addr  
          super().__init__(_socket)
          self.preauth_url_maps = {"/signup" : self.signup , "/login" : self.login }
          self.url_maps = { "/test" : self.test , "/send_msg"  : self.send_msg , "/read_reciept" : self.read_reciept , 
                            "/create_group" : self.create_group , "/add_members" : self.add_members ,
                             "/set_public_key" : self.set_public_key , 
                             "/get_public_key" : self.get_public_key , "/send_key" : self.send_key   }
          self.clients = clients

      def login(self,data,headers) :
          isLogged = user_db.logInUser(data["user"],data["password"],self.addr[1]) 
          if isLogged :
            self.is_authorised = True 
          self.user = data['user']
          self.clients[self.user] = self  
          self.add_send_queue("/login_res", isLogged)
          thread = threading.Thread(target = self.intial_send )
          thread.start()
          return isLogged
          
      def signup(self,data,headers):
          isCreated = user_db.signUpUser(data["user"],data["password"])
          if isCreated : 
             self.login(data,headers)
          self.add_send_queue("/signup_res", isCreated)

      def set_public_key(self,key,headers) : 
          msg_db.addPublicKey(self.user,key)

      def get_public_key(self,user,headers) :
          if type(user) == dict : 
            self.add_send_queue("/public_key_response",{ "user" : user["user"] , "group" : user["group"] ,  "key" : msg_db.getPublicKey(user["user"])  } )
          else : 
            self.add_send_queue("/public_key_response",{ "user" : user , "key" : msg_db.getPublicKey(user)} )
      
      def send_key(self,data,headers) : 
          self.clients[data["to"]].add_send_queue("/set_secret_key",data)

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
            if reciever in self.clients :  #to be replaced 
               new_data = { "sender" : self.user , "msg" : data["msg"] , "id" : id  , "sent" : t , "group" :  to if isGroup else False ,
                             "type" : data["type"]  }
               self.clients[reciever].add_send_queue("/recieve_msg",new_data)
      
      def read_reciept(self,data,headers) :
          id , sender  = data["id"] , data["sender"]
          if data["group"] : 
             msg_db.updateCount(id,sender,self.user)
          else : 
            msg_db.updateTimeRecieved(id,sender,self.user,data["time"])
            if sender in self.clients :
               self.clients[sender].add_send_queue("/read_reciept", {"time" : data["time"] , "id" : id , "level" :2 },
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

class Server(socket.socket) : 
    
    def __init__(self,server_address,clients) : 
        super().__init__(socket.AF_INET, socket.SOCK_STREAM )
        server_address = ('localhost', server_address)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(server_address)
        self.listen(100)
        self.addr = server_address
        self.clients = clients
        self.count_active_conn = 0 

    def start(self) : 
        while True:
           connection, client_address = self.accept()
           print('Connection from', client_address , " to ", self.addr )
           client_thread = threading.Thread(target=client_handle,args=(connection,client_address,self.clients))
           client_thread.start()
           self.count_active_conn += 1 
        