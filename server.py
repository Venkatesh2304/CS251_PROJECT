

import socketserver
from tabnanny import check
import threading
import socket
import time 
from Socket import Socket
import pandas as pd 


users = {"1" :"1", "2":"1" , "3" : "1" , "4":"1"}
    
clients = {}



class DB(pd.DataFrame) :
      def  __init__(self) : 
          super().__init__([],columns = ["id","_id","sender","reciever","msg","sent","recieved"])
      def add_msg(self,_id,sender,reciever,msg,time) :
          id = 1 if len(self.index) == 0 else self.index[-1] + 2 
          self.loc[len(self)] = [id,_id,sender,reciever,msg,time,None]
          return int(id) 
      def delete_msg(self,id) : 
          self = self[self.id != id ]
      def update_recieve_time(self,id,time) : 
          self.loc[self.id == id, 'recieved'] = time 
      def get_sender(self,id) :
          return self[self.id == id]["sender"].iloc[0]
      def get_unread_msg(self,reciever) :
          return self[(self.reciever == reciever) & (self.recieved.isna()) ].to_dict(orient="records")
      def get_read_reciept(self,sender) : 
          return self[(self.sender == sender) & (self.recieved.notna()) ].to_dict(orient="records")
          
def client_handle(conn,addr) : 
    connection = ClientConnection(conn,addr)
    connection.start()

def create_user(user,password) : 
    if user not in users : 
       users[user] = password 
       return True 
    return False 

def check_user(user,password,conn) :
    if user in users and users[user] == password : 
        return True 
    else : 
        return False 

db = DB()
# Create a TCP/IP socket
class ClientConnection(Socket) : 
      def __init__(self, _socket , addr = None ):
          self.addr = addr  
          self.db = db
          super().__init__(_socket)
          self.preauth_url_maps = {"/signup" : self.signup , "/login" : self.login }
          self.url_maps = { "/test" : self.test , "/send_msg"  : self.send_msg , "/read_reciept" : self.read_reciept }
      
      def login(self,data,headers) : 
          isLogged = check_user(data["user"],data["password"],self.addr)
          if isLogged :
            self.is_authorised = True 
          self.user = data['user']
          clients[self.user] = self  
          self.add_send_queue("/login_res", isLogged)
          thread = threading.Thread(target = self.intial_send )
          thread.start()
          return isLogged

      def signup(self,data,headers):
          isCreated = create_user(data["user"],data["password"])
          self.add_send_queue("/signup_res", isCreated)
      
      def send_msg(self,data,headers) :
          _id , to = data["_id"] , data["to"]
          time.sleep(0.01)
          t = time.time()
          new_id = self.db.add_msg(_id,self.user,data["to"],data["msg"],t)
          self.add_send_queue("/read_reciept", {"time" : t ,"_id": _id , "id" : new_id , "level" : 1 })
          if to in clients : 
              new_data = { "sender" : self.user , "msg" : data["msg"] , "id" : new_id , "sent" : t }
              clients[to].add_send_queue("/recieve_msg",new_data)
          
      def read_reciept(self,data,headers) :
          id  = data["id"]
          sender = self.db.get_sender(id)
          self.db.update_recieve_time(id,data["time"])
          if sender in clients :
              clients[sender].add_send_queue("/read_reciept", {"time" : data["time"] , "id" : id , "level" :2 },{},lambda :lambda : self.db.delete_msg(id)  )

      def intial_send(self) : 
          unread_msgs = self.db.get_unread_msg(self.user)
          reciepts = self.db.get_read_reciept(self.user)
          if len(unread_msgs) :
             self.add_send_queue("/recieve_msg", unread_msgs)
          if len(reciepts):
            x = [ i["id"] for i in reciepts ] 
            self.add_send_queue("/read_reciept", { "reciepts" : reciepts , "level" :2 },{}, lambda : x.map( lambda p : self.db.delete_msg(p)) )

      def test(self,data,headers) : 
          if data.count("test messsage number") != 1000 : 
              raise Exception("full not recieved" + data[:10])
          print('received {!r}'.format(data.replace("test messsage number","")) + " :: " + str(self.addr[1]) + " :: " + str(headers) ) 
        
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(server_address)

sock.listen(100)

while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)
        print("thread started")
        client_thread = threading.Thread(target=client_handle,args=(connection,client_address))
        client_thread.start()
        