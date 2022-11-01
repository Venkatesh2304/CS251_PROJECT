

import socketserver
import threading
import socket
from Socket import Socket 
def client_handle(conn,addr) : 
    connection = Server(conn,addr) 
    connection.start()

users = [["ven","121"],["ven","122"],["ven","123"]]


# Create a TCP/IP socket
class Server(Socket) : 
      def __init__(self, _socket , addr = None ):
          self.addr = addr  
          super().__init__(_socket)
          self.url_maps = { "/test" : self.test }
      
    #   def login(self,data,headers) :  
    #        user,password = data["user"] , data["password"] 
    #        if [user,password] in users : 
            
      def test(self,data,headers) : 
          if data.count("test messsage number") != 1000 : 
              raise Exception("full not recieved" + data[:10])
          print('received {!r}'.format(data.replace("test messsage number","")) + " :: " + str(self.addr[1]) + " :: " + str(headers) ) 
        

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(100)

while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)
        print("thread started")
        client_thread = threading.Thread(target=client_handle,args=(connection,client_address))
        client_thread.start()
        