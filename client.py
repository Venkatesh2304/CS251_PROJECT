import socket
import sys
import time 
def send_t(msg) :
    message = ("client msg " +  str(sys.argv[1])).encode()
    print('sending {!r}'.format(message) + "-" + str(sys.argv[1]))
    sock.send(message)
    data = sock.recv(1024)
    print('received {!r}'.format(data) + "-" + str(sys.argv[1]))
    time.sleep(0.5)


# class  Client(socket.socket) : 
#        def Send(data) :
#            MAX_BUFFER = 1024  
#            data_length = len(data)
#            headers = "" 
#            sent = 0 
#            while sent < data_length : 
                 

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
for i in range(4) :

input()

      
# import socket
# import socketserver


# class Socket(socket.socket) : 
#     _MSGLEN = 100000000 
#     def send(self, msg):
#         msg = msg.encode()
#         totalsent = 0
#         while totalsent < len(msg) :
#             sent = super().send(msg[totalsent:])
#             if sent == 0:
#                 raise RuntimeError("Socket Broken")
#             totalsent = totalsent + sent
    
#     def recieve(self):
#         chunks = []
#         bytes_recd = 0
#         while bytes_recd < self._MSGLEN :  
#             chunk = super().recv(min(self._MSGLEN - bytes_recd, 2048))
#             if chunk == b'':
#                 raise RuntimeError("socket connection broken")
#             chunks.append(chunk)
#             bytes_recd = bytes_recd + len(chunk)
#         return (b''.join(chunks)).decode()

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("localhost",8080))
# while True : 
#     x = input("enter msg ::")
#     client.send(x.encode())
#     print(client.recv(1024).decode())