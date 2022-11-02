

import socketserver
from tabnanny import check
import threading
import socket
import time 
from Socket import Socket

users = {"ven" :"121", "aad":"122" , "yash" : "123"}

class DB() : 
      _msg = []
      def add_msg(self,to,msg) :
          _id = len(self._msg) 
          self._msg.append(to + " ==> " + msg)
          return _id 



def client_handle(conn,addr) : 
    connection = Server(conn,addr)
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

sent = {}
rec = {}

# Create a TCP/IP socket
class Server(Socket) : 
      def __init__(self, _socket , addr = None ):
          self.addr = addr  
          super().__init__(_socket)
          self.preauth_url_maps = {"/signup" : self.signup , "/login" : self.login }
          self.url_maps = { "/test" : self.test , "/send_msg"  : self.send_msg }
      
      def login(self,data,headers) : 
          isLogged = check_user(data["user"],data["password"],self.addr)
          if isLogged :
            self.is_authorised = True 
          self.add_send_queue("/login_res", isLogged)
          return isLogged
      def signup(self,data,headers):
          isCreated = create_user(data["user"],data["password"])
          self.add_send_queue("/signup_res", isCreated)
            
      def send_msg(self,data,headers) :
          _id = data["id"]
          time.sleep(0.01)
          
          self.add_send_queue("/read_reciept", {"time" : time.time() } ,{ "id": _id })    
      

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
        