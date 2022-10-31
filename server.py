
import socket
import threading
def client_handle(connection,addr) : 
    while True : 
          data = connection.recv(1024)
          print('received {!r}'.format(data) + " :: " + str(addr[1]) )
          connection.sendall(b"server recieved successfully")
    #connection.close()
        
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)
        print("thread started")
        client_thread = threading.Thread(target=client_handle,args=(connection,client_address))
        client_thread.start()
        
  


# import socket
# import threading

# def client_handler(serversocket) : 
#     #client = socket.socket()
#     #msg = client.recv(1024).decode()
#     #print(addr,  msg)
#    while True :
#     print(1)
#     (client,addr) = serversocket.accept()
#     print(2)
#     client.send(("a"*100).encode())
#     print(3)

# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.bind(("localhost",8080))
# serversocket.listen(5)
# t = threading.Thread(target=client_handler,args=(serversocket,))
# t.start()

#     # print(2)
#     # (client,addr) = serversocket.accept()
#     # print(1)
#     # client.send(("a"*100000000).encode())
#     # print(3)

# #client_handler(client,addr)
#     #client_thread = threading.Thread(target=client_handler,args=(client,addr))
#     #client_thread.start()
