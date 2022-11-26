import base64
from base64 import urlsafe_b64encode, urlsafe_b64decode
from datetime import datetime
import json
import os
import socket
import time 
from Socket import Socket 
import msg_client as db 
from termcolor import colored
import logging
import binascii
from Crypto.Cipher import AES
from collections import defaultdict
import rsa
from Crypto import Random


def b2a(binary) : 
    return base64.b64encode(binary).decode()

def a2b(text) : 
    return base64.b64decode(text)

error = lambda t : colored(t,"red")
succ = lambda t : colored(t,"green")
padding_character = b"{"
pkey_e = 65537 

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

base64pad = lambda s: s + b'=' * (4 - len(s) % 4)
base64unpad = lambda s: s.rstrip(b"=")

rsa_key_size = 2048
server_address = ('localhost', 10000)

class Client(Socket) : 
      
      def __init__(self, _socket , user , addr = None ):
          self.addr = addr    
          self.user =  user
          super().__init__(_socket)
          self.url_maps = { "/login_res" : self.login_res , "/signup_res" : self.signup_res , 
                            "/read_reciept" : self.read_reciept , "/recieve_msg": self.recieve_msg ,  "/ack" : self.ack , 
                            "/public_key_response" : self.public_key_response , "/set_secret_key" : self.set_secret_key}
          self.preauth_url_maps = self.url_maps
          self.wait_public_key = defaultdict(list)
          self.wait_secret_key = defaultdict(list)

      def block(self) : 
          self.is_blocked = True 

      def encrypt(self,msg, secret_key):
           iv = Random.new().read(BS)
           cipher = AES.new(secret_key, AES.MODE_CFB, iv)
           encrypted_msg = cipher.encrypt( pad(msg).encode() )
           return base64unpad(urlsafe_b64encode(iv + encrypted_msg)).decode()

      def decrypt(self,msg,secret_key) : 
           decoded_msg = urlsafe_b64decode(base64pad(msg.encode()))
           iv = decoded_msg[:BS]
           encrypted_msg = decoded_msg[BS:] 
           cipher = AES.new(secret_key, AES.MODE_CFB, iv)
           return unpad(cipher.decrypt(encrypted_msg)).decode()
        
      def generatekey(self) : 
           return  os.urandom(16)
     
      def login_req(self,user,password) :
          self.db = db.clientDB(user)
          self.user = user 
          with open(self.user+".pem","rb") as f : 
               self.private_key =  rsa.PrivateKey.load_pkcs1(f.read())
          if not os.path.exists(user) : 
              os.makedirs(user)
          logging.basicConfig(filename=f"out_{user}",level=logging.DEBUG)
          self.add_send_queue("/login",{"user" : user , "password" : password})
          
      def login_res(self,data,headers) : 
          if data :
            print("You are logged in")
          else : 
            print("Credientials is wrong")
      
      def signup_req(self,user,password) :
          self.db = db.clientDB(user)
          self.user = user 
          if not os.path.exists(user) : 
              os.makedirs(user)
          logging.basicConfig(filename=f"out_{user}",level=logging.DEBUG)
          self.add_send_queue("/signup",{"user" : user , "password" : password},{},lambda : self.block)
                    
      def signup_res(self,data,headers) : 
          self.is_blocked = False 
          if data :
              print("User created") 
          else : 
             print("Already exists. Problem in Signup")
          (self.public_key , self.private_key) = rsa.newkeys(rsa_key_size)
          with open(self.user+".pem","wb+") as f : 
               f.write( self.private_key.save_pkcs1() )
          self.add_send_queue("/set_public_key", self.public_key.n) 

      #get public key if  secret key no exists    
      def send_msg(self,to,msg,isGroup=False,fname=False,headers ={}) :
          
          if fname : 
             if not os.path.exists(fname) : 
                self.print(error(f"The {fname} doesnt exists"))
             with open(fname,"rb") as f : 
                msg =  binascii.b2a_base64(f.read()).decode()
              
          fname = fname if fname else "text"    #default is text if no file is given 
          id = self.db.addSentMsg(to,msg,fname) 
          msg = { "id": id  , "to" : to , "msg" : msg  , "group" : isGroup , "type" : fname }
          secret_key = self.db.get_secret_key(to,isGroup)
          #print( self.user , to  , secret_key , "11111")
          if not secret_key : #generate key 
             self.wait_public_key[to].append(msg)
             self.add_send_queue("/get_public_key",to)
          else : 
            msg["msg"]  =  self.encrypt(msg["msg"],secret_key)
            logging.debug(f"sent {time.time()}")
            #print("sent")
            self.add_send_queue("/send_msg",msg,headers)
          
      def recieve_msg(self,data,headers) : 
          t = time.time()
          data = data if type(data) == list else [data]
          for data in data :
                logging.debug(f"receive {time.time()}") 
                sender , group  = data["sender"] , data["group"]
                _sender = group if group else sender
                secret_key = self.db.get_secret_key(_sender,data["group"])
                #print( _sender , secret_key )
                if not secret_key : 
                   print(1)
                   self.wait_secret_key[_sender].append(data)
                   return True 
                data['msg'] = self.decrypt(data['msg'],secret_key)
                msg = data["msg"]
                if data["type"] != "text" : 
                   with open( self.user + "/" + data["type"] ,"wb+") as f  : 
                         f.write( binascii.a2b_base64( data["msg"].encode() ) )
                   msg = "File ==> "+ data["type"]
                
                if group :
                    self.print(f"""{ colored(sender+" sent on "+group+":: ","green") }{msg}{ " "*3 + colored(datetime.fromtimestamp(data['sent']).strftime("%H:%M:%S"),"yellow")  }    """)
                else : 
                    self.print(f"""{ colored(sender+" sent :: ","green" ) }{msg}{ " "*3 + colored(datetime.fromtimestamp(data['sent']).strftime("%H:%M:%S"),"yellow")  }    """)
                
                self.add_send_queue("/read_reciept", {"id": data['id'] , "time": t , "sender" : data["sender"] , "group" : bool(data["group"]) })
                self.db.addRecvMsg( data["id"] , data["sent"] , data["msg"] , t , "text" )

      def read_reciept(self,data,headers) : 
          level = data["level"]
          ( type , msg , reciever ) = self.db.getMsgSent(data["id"])
          if type != "text" : 
             msg = "File :: " + type 
          if level == 0 : 
             self.print(error(f"Error Sending Message to the Server :: {msg} "))
          else :
            if level == 1 :     
              self.db.updateTimeSent( data["id"] , data["time"] )
              self.print( colored("Server Received :: ","blue") + msg +  " "*3 + colored(datetime.fromtimestamp(data['time']).strftime('%H:%M:%S'),"yellow") ) 
            elif level == 2  : 
               if "reciepts" in data : 
                 for data in data["reciepts"] : 
                   self.print( colored(reciever+" Received :: ","blue") + msg +  " "*3 + colored(datetime.fromtimestamp(data['time']).strftime('%H:%M:%S'),"yellow")) 
                   self.db.updateTimeRecieved(data["id"],data["time"])                    
               else : 
                   self.print( colored(reciever+" Received :: ","blue") + msg +  " "*3 + colored(datetime.fromtimestamp(data['time']).strftime('%H:%M:%S'),"yellow")) 
                   self.db.updateTimeRecieved(data["id"],data["time"])                    
            else : 
                pass 
      
      #generate a secret key and encrypt it using the response public key 
      def public_key_response(self,data,headers)  : 
          isGroup =  "group" in data.keys()
          to  , public_key = data["user"] , data["key"]
          if not  public_key : 
             self.print(colored( f"User {to} doesn't exists . So, message aborted " , "red" ))
             return 
          public_key =  rsa.PublicKey(public_key,pkey_e) #public_key is integer 
          if isGroup : 
              group = data["group"]
              secret_key = self.db.get_secret_key(group,True)
              sender = group 
          else :
              secret_key = self.generatekey() #return bytes key
              self.db.add_secret_key(to,secret_key,False) 
              sender = self.user  
          enc_key =  b2a(rsa.encrypt(secret_key,public_key)) 
          self.add_send_queue("/send_key",{ "sender":sender,"to":to,"key":enc_key, "group" : isGroup })
          #print(sender,to)
          for msg in self.wait_public_key[to] : 
              msg["msg"]  =  self.encrypt( msg["msg"] , secret_key)
              #print("unsend")
              self.add_send_queue("/send_msg",msg) #default headers 
          del self.wait_public_key[to] 
      
      #set the secret key using the encrypted send 
      def set_secret_key(self,data,headers) : 
          sender , encrypted_key = data["sender"] , data["key"] 
          key = rsa.decrypt( a2b(encrypted_key) , self.private_key )
          self.db.add_secret_key(sender,key,data["group"])
          #print(sender,data)
          for msg in self.wait_secret_key[sender] : 
              self.recieve_msg(msg,{})
              pass 
          del self.wait_secret_key[sender]
            
      #groups 
      def ack(self,data,headers) : 
          self.is_blocked = False  
          
      def create_group(self,gname)  : 
          self.add_send_queue("/create_group",{"gname" : gname},{},self.block)
          secret_key = self.generatekey() #return bytes key
          self.db.add_secret_key(gname,secret_key,True) 
        
      def add_members(self,gname,members) : 
          members  =  [members] if type(members) != list else members 
          self.add_send_queue("/add_members",{"gname":gname,"members":members},{},self.block)
          for member in members : 
             self.add_send_queue("/get_public_key",{"user":member,"group":gname})

      def print(self,*args) : 
          #logging.info(" ".join(args))   
          print(*args)    


err = True 
for retry_times in range(90) : 
   try : 
      super_server_port = ("localhost",10000)
      basic_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      basic_sock.connect(super_server_port)
      server_address = tuple( json.loads(basic_sock.recv(1024).decode()) ) 
      err = False 
      break 
   except Exception as e : 
      time.sleep(1)

if not err : 
    err = True 
    
    for retry_times in range(90) : 
      try :
         sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) , 1)
         sock.connect(server_address)
         sock.start()
         err = False 
         break 
      except : 
          pass 
    
    if not err : 
        print(colored(f"You are connected to the server :: {server_address[0]}","green")) 
        
        if input("Enter l for login and s for signup") != "s" : 
           sock.login_req(input("User : \n"),input("Password : \n"))
        else :
            sock.signup_req(input("User : \n"),input("Password : \n"))
        
        while True : 
           inputs =  {  "Send" :  sock.send_msg , "SendGroup" : lambda to,msg : sock.send_msg(to,msg,True) , "CreateGroup" : sock.create_group ,
                        "AddMember" : sock.add_members  , "SendFile" : lambda to,fname : sock.send_msg(to,"",False,fname) , 
                        "SendGroupFile" : lambda to,fname : sock.send_msg(to,"",True,fname) } #"PrintRecieved" : sock.print_recv , "PrintSent" : sock.print_sent }     
           i = input("")
           func = i.split(' ')[0]
           if i == "Exit" : 
              break 
           if func  in inputs :
              try :
                 inputs[func]( *tuple( i.split(" ")[1: ] ) )
              except Exception as e : 
                  logging.debug(e) 
           else : 
              continue 
    else : 
        print(colored("Maximum Retry exceeded for connection with server. Close and Try again","red"))
else  :
        print(colored("Maximum Retry exceeded for connection with server. Close and Try again","red"))



# x = []
# x += ["CreateGroup test","AddMember test atishay","AddMember test aadithya"]
# x += ["SendGroup test hi,guys"]
# x += ["Send aadithya t"]

        # time.sleep(0.5)
     #  if count >= len(x) : 
     #     break 
     #  i = x[count]
     #  count += 1 
    #  i = input("")
    #  if i == "-1" : 
    #     break 
    #  j = input("")
    #  sock.send_msg(i,j)   

