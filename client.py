import base64
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
from cryptography.fernet import Fernet
from collections import defaultdict
import rsa

def b2a(binary) : 
    return base64.b64encode(binary).decode()

def a2b(text) : 
    return base64.b64decode(text)


padding_character = b"{"
e = 65537 
rsa_key_size = 2048
server_address = ('localhost', 10000 )

class Client(Socket) : 
      
      def __init__(self, _socket , user , addr = None ):
          self.addr = addr    
          self.user =  user
          super().__init__(_socket)
          self.url_maps = { "/login_res" : self.login_res , "/signup_res" : self.signup_res , 
                            "/read_reciept" : self.read_reciept , "/recieve_msg": self.recieve_msg ,  "/ack" : self.ack , 
                            "/public_key_response" : self.public_key_response }
          self.preauth_url_maps = self.url_maps
          self.wait_public_key = defaultdict(list)
          self.wait_secret_key = defaultdict(list)

      def block(self) : 
          self.is_blocked = True 

      def encrypt(self,msg, secret_key):
           cipher = AES.new(secret_key,AES.MODE_EAX)
           padded_private_msg = msg + (padding_character * ((16-len(msg)) % 16))
           encrypted_msg = cipher.encrypt(padded_private_msg)
           encrypted_msg = base64.b64encode(encrypted_msg).decode()
           return encrypted_msg
      
      def decrypt(self,msg,secret_key) : 
           encrypted_msg = base64.b64decode(msg) #return bytes of the encrypted message 
           cipher = AES.new(secret_key) 
           decrypted_msg = cipher.decrypt(encrypted_msg) 
           unpadded_private_msg = decrypted_msg.rstrip(padding_character)
           return unpadded_private_msg
      
      def generatekey(self) : 
          #return Fernet.generate_key()
           return  os.urandom(16)
      def login_req(self,user,password) :
          self.db = db.clientDB(user)
          self.user = user 
          if not os.path.exists(user) : 
              os.makedirs(user)
          logging.basicConfig(filename=f"out_{user}",level="INFO")
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
          self.add_send_queue("/signup",{"user" : user , "password" : password},{},lambda : self.block)
                    
      def signup_res(self,data,headers) : 
          self.is_blocked = False 
          if data :
              print("User created") 
          else : 
             print("Already exists. Problem in Signup")
          (self.public_key , self.private_key) = rsa.newkeys(rsa_key_size)
          self.add_send_queue("/set_public_key", self.public_key.n) 

      #get public key if  secret key no exists    
      def send_msg(self,to,msg,isGroup=False,fname=False,headers ={}) :
          if fname : 
             with open(fname,"rb") as f : 
                msg =  binascii.b2a_base64(f.read()).decode()
          fname = fname if fname else "text"
          id = self.db.addSentMsg(to,msg,fname)
          msg = { "id": id  , "to" : to , "msg" : msg  , "group" : isGroup , "type" : fname }
          secret_key = self.db.get_secret_key(to)
          if not secret_key : #generate key 
             self.wait_public_key[to].append(msg)
             self.add_send_queue("/get_public_key",to)
             print(111)
          else : 
            msg["msg"]  =  self.encrypt(msg["msg"],secret_key)
            self.add_send_queue("/send_msg",msg,headers)
          
      def recieve_msg(self,data,headers) : 
          t = time.time()
          data = data if type(data) == list else [data]
          for data in data : 
                to = data["to"]
                secret_key = self.db.get_secret_key(to)
                if not secret_key : 
                   self.wait_secret_key[to].append(data)
                   return True 
                msg = data["msg"]
                if data["type"] != "text" : 
                   with open( self.user + "/" + data["type"] ,"wb+") as f  : 
                         f.write( binascii.a2b_base64( data["msg"].encode() ) )
                   msg = "File ==> "+ data["type"]
                self.print(colored("You have recieved a message from","blue") + f""":: {data['sender']} , msg :: {msg} , time :: { datetime.fromtimestamp(data['sent']).strftime("%H:%M:%S")  }    """)
                self.add_send_queue("/read_reciept", {"id": data['id'] , "time": t , "sender" : data["sender"] , "group" : bool(data["group"]) })
                self.db.addRecvMsg( data["id"] , data["sent"] , data["msg"] , t , "text" )

      def read_reciept(self,data,headers) : 
          level = data["level"]
          ( type , msg ) = self.db.getMsgSent(data["id"])
          if type != "text" : 
             msg = "File ==> " + type 
          if level == 0 : 
             self.print(f"Error Sending Message to the Server :: {msg} ")
          else :
            if level == 1 :     
              self.db.updateTimeSent( data["id"] , data["time"] )
              self.print( colored("Your message has been sent to server","yellow") ,f":: {msg} , sent time :: {datetime.fromtimestamp(data['time']).strftime('%H:%M:%S')}") 
            elif level == 2  : 
               if "reciepts" in data : 
                 for data in data["reciepts"] : 
                   self.print( colored("Your message has been sent to the reciever","green") +f":: {msg} , sent time :: {datetime.fromtimestamp(data['time']).strftime('%H:%M:%S')}") 
                   self.db.updateTimeRecieved(data["id"],data["time"])                    
               else : 
                   self.print( colored("Your message has been sent to the reciever","green") +f":: {msg} , sent time :: {datetime.fromtimestamp(data['time']).strftime('%H:%M:%S')}") 
                   self.db.updateTimeRecieved(data["id"],data["time"])                    
            else : 
                pass 
      
      #generate a secret key and encrypt it using the response public key 
      def public_key_response(self,data,headers)  : 
          to , public_key = data["user"] , rsa.PublicKey(data["key"],e) #public_key is integer 
          print(" user public_key :: ", to , public_key )
          secret_key = self.generatekey() #return bytes key 
          print( secret_key , public_key)
          enc_key =  b2a(rsa.encrypt(secret_key,public_key)) 
          self.add_send_queue("/send_key",{"to":to,"enc_key":enc_key})
          self.db.add_secret_key(to,secret_key) 
          for msg in self.wait_public_key[to] : 
              msg["msg"]  =  self.encrypt( msg["msg"].encode() ,secret_key)
              print(" final e2e msg :: " , msg["msg"])
              self.add_send_queue("/send_msg",msg) #default headers 
      
      #set the secret key using the encrypted send 
      def set_secret_key(self,data,headers) : 
          to , encrypted_key = data["to"] , data["key"]
          key = rsa.decrypt( a2b(encrypted_key) , self.private_key )
          self.db.add_secret_key(to,key)
          for msg in self.wait_secret_key[to] : 
              self.recieve_msg(msg,{})
            

      #groups 
      def ack(self,data,headers) : 
          self.is_blocked = False  
          
      def create_group(self,gname)  : 
          self.add_send_queue("/create_group",{"gname" : gname},{},self.block)
      
      def add_members(self,gname,members) : 
          members  =  [members] if type(members) != list else members 
          self.add_send_queue("/add_members",{"gname":gname,"members":members},{},self.block)

      def print(self,*args) : 
          #logging.info(" ".join(args))   
          print(*args)    



sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) , 1)
sock.connect(server_address)
sock.start()
#sock.login_req(input("User : \n"),input("Password : \n"))
sock.signup_req(input("User : \n"),input("Password : \n"))
count  = 0 


while True : 
     inputs =  { "Send" :  sock.send_msg , "SendGroup" : lambda to,msg : sock.send_msg(to,msg,True) , "CreateGroup" : sock.create_group ,
                  "AddMember" : sock.add_members  , "SendFile" : lambda to,fname : sock.send_msg(to,"",False,fname) , 
                  "SendGroupFile" : lambda to,fname : sock.send_msg(to,"",True,fname) } #"PrintRecieved" : sock.print_recv , "PrintSent" : sock.print_sent }     
     
     i = input("")
     func = i.split(' ')[0]
     if func  in inputs :
        inputs[func]( * tuple( i.split(" ")[1: ] ) )
     else : 
      time.sleep(10)
      break 
   




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

