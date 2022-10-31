
import socketserver
import threading
import socket
from Socket import Socket 
def client_handle(conn,addr) : 
    connection = Socket(conn) 
    while True : 
          (ctype , data)  =  connection.Recv()
          data = data.decode()
          if data.count("test messsage number") != 1000 : 
              raise Exception("full not recieved" + data[:100])
          print('received {!r}'.format(data.replace("test messsage number","")) + " :: " + str(addr[1]) )
        
# Create a TCP/IP socket
class Server(Socket) : 
      pass 

sock = Server( socket.socket(socket.AF_INET, socket.SOCK_STREAM) )

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
        