import socket
class  Socket() : 
       MAX_BUFFER = 1024
       SEND_LEN = 1024 
       length_LEN = 10 
       HEADER_LEN = 11 
       def __init__(self,_socket) :
           self.socket = _socket 
       def __getattr__(self,name) : 
           if name in self.__dict__ :  
              return  self.__dict__[name] 
           return self.socket.__getattribute__(name) 
       def parse_header(self,header) : 
           header = header.decode()
           return ( header[0] , int(header[1:].lstrip()) )
       def Send(self,data) :
           data_length =  len(data)
           len_str = str(data_length).zfill(self.length_LEN)
           headers =  (f"t{len_str}").encode()
           self.socket.sendall(headers)
           self.socket.sendall(data)
       def recv(self,length) :
           recv = 0
           chunks = []
           if recv < length : 
              chunk = self.socket.recv(length-recv) 
              if not chunk : 
                 raise Warning("Connection closed abruptly")
              recv += len(chunk) 
              chunks.append(chunk)
           return b"".join(chunks) 
       def Recv(self) : 
           header = self.socket.recv(self.HEADER_LEN)
           ctype , length = self.parse_header(header)
           return ( ctype , self.recv(length) )
             
