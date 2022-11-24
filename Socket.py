import queue
import socket
import json 
import threading
import zlib 
import warnings
import time 

warnings.simplefilter("ignore")
# warnings.simplefilter(action='ignore', category=FutureWarning)

class  Socket() : 
       MAX_BUFFER = 1024
       SEND_LEN = 1024 
       length_LEN = 10 
       HEADER_LEN = 10
       _headers = { "ctype" : "text" }

       def __init__(self,_socket) :
           self.socket = _socket 
           self.id = 0
           self.is_authorised = False 
           self.is_blocked = False 

       def start(self) : 
           self.send_threads = queue.Queue()
           self.send_main_worker = threading.Thread(target=self.Send_Worker)
           self.send_main_worker.start()
           self.recieve_worker = threading.Thread(target=self.Recv_Worker)
           self.recieve_worker.start()
       def __getattr__(self,name) : 
           if name in self.__dict__ :  
              return  self.__dict__[name] 
           return self.socket.__getattribute__(name) 
       def parse_header(self,header) : 
           header = header.decode()
           return ( header[0] , int(header[1:].lstrip()) )
       
       #send functions 
       #add to the send threads 
       def add_send_queue(self,url,body,headers = {},do=lambda : 0 ) : 
           self.send_threads.put((url,body,headers,do))
       #main worker which keeps looking for any send and then sends it in order 
       def Send_Worker(self) : 
           while True : 
             args = self.send_threads.get()
             while self.is_blocked : 
                   time.sleep(0.01)
             self.Send(*args)
             self.send_threads.task_done()
        
       #The customised Send function which sends a given message 
       def Send(self,url,body,headers,do) :
           #make the request data
           data = { "url" : url , "body" : body }
           headers.update(self._headers)
           data.update(headers) 
           try :
             data = json.dumps(data).encode()
           except Exception as e : 
              print(data,e)
           data = zlib.compress(data)
           #find and send the length of the data 
           data_length =  len(data)
           len_str = str(data_length).zfill(self.length_LEN).encode()
           #print(len_str)
           
           self.socket.sendall(len_str)
           self.socket.sendall(data)
           do() 

       def handle_body(self,data) : 
           body = data["body"]
           del data["body"]
           return body
       #recieve functions 
       def recv(self,length,decompress=True) :
           recv = 0
           chunks = []
           while recv < length : 
              chunk = self.socket.recv(length-recv) 
              if not chunk : 
                 raise Warning("Connection closed abruptly")
              recv += len(chunk) 
              chunks.append(chunk)
           #print("Recv :: ", b"".join(chunks) )
           if decompress : 
             return zlib.decompress(b"".join(chunks)).decode() 
           else : 
              return b"".join(chunks).decode()

       def Recv(self) : 
           length = int( self.recv(self.HEADER_LEN, decompress=False).lstrip() )
           data = json.loads( self.recv(length) ) 
           body = self.handle_body(data)
           url = data["url"]
           #print(url)
           if not self.is_authorised :
              if url in self.preauth_url_maps : 
                return self.preauth_url_maps[url](body,data)
              else : 
                raise Exception(407)          
           if  url in self.url_maps : 
              thread = threading.Thread( target = self.url_maps[url] , args = (body,data)) 
              thread.start()
              return thread 
           else : 
               raise Exception(400)

       def Recv_Worker(self) : 
           while True : 
               self.Recv()
