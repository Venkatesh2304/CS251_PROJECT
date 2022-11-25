import socket 
import threading
from server import *
from Socket import Socket
import json 

class SuperServer(socket.socket) : 
      def __init__(self,m) : #m is number of servers 
          super().__init__(socket.AF_INET, socket.SOCK_STREAM )
          server_address = ('localhost', 10000)
          self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          self.bind(server_address)
          self.listen(100)   
          self.clients = {}
          self.servers = [] 
          self.threads = []
          for i in range(m) : 
              port = 10001 + i 
              server  = Server(port,self.clients)
              self.servers.append( server )
      
      def send_assigned_server(self,conn) :
           print(2)
           counts = [ server.count_active_conn for server in self.servers ]
           best_server_addr = self.servers[counts.index( min(counts) )].addr
           conn.sendall( json.dumps(best_server_addr).encode() )
        
      def start(self) : 
          for server in self.servers : 
              server_thread = threading.Thread(target= server.start)
              server_thread.start()
              self.threads.append( server_thread )
          while True:
            connection, client_address = self.accept()
            client_thread = threading.Thread(target= self.send_assigned_server ,args=(connection,))
            client_thread.start()

s = SuperServer(5)
s.start()
        

      
          