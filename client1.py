from datetime import datetime
import socket
import time 
from Socket import Socket 
import msg_client as db 
from termcolor import colored
import logging


server_address = ('localhost', 10000 )

class Client(Socket) : 
      
      def __init__(self, _socket , user , addr = None ):
          self.addr = addr    
          self.user =  user
          super().__init__(_socket)
          self.url_maps = { "/login_res" : self.login_res , "/signup_res" : self.signup_res , 
                            "/read_reciept" : self.read_reciept , "/recieve_msg": self.recieve_msg}
          self.preauth_url_maps = self.url_maps

      def login_req(self,user,password) :
          self.db = db.clientDB(user)
          logging.basicConfig(filename=f"out_{user}",level="INFO")
          self.add_send_queue("/login",{"user" : user , "password" : password})
      def login_res(self,data,headers) : 
          if data : 
            print("You are logged in")
          else : 
            print("Credientials is wrong")
      def signup_req(self,user,password) : 
          self.add_send_queue("/signup",{"user" : user , "password" : password})
      def signup_res(self,data,headers) : 
          if data :
            print("User created") 
          else : 
             print("Already exists")
      def send_msg(self,to,msg,isGroup=False,fname=False,headers ={}) :
          if fname : 
             with open(fname) as f : 
                msg =  f.read()
          fname = fname if fname else "text"
          id = self.db.addSentMsg(to,msg,fname)
          msg = {  "id": id  , "to" : to , "msg" : msg  , "group" : isGroup , "type" : fname }
          self.add_send_queue("/send_msg",msg,headers)
      def recieve_msg(self,data,headers) : 
          t = time.time()
          data = data if type(data) == list else [data]
          for data in data : 
                msg = data["msg"]
                if data["type"] != "text" : 
                   with open( data["sender"]+" "+data["receiver"] + " " + data["fname"],"wb+") as f  : 
                         f.write(data["msg"])
                   msg = "File ==> "+ data["sender"]+" "+data["receiver"] + " " + data["fname"]
                self.print(colored("You have recieved a message from","blue") + f""":: {data['sender']} , msg :: {msg} , time :: { datetime.fromtimestamp(data['sent']).strftime("%H:%M:%S")  }    """)
                self.add_send_queue("/read_reciept", {"id": data['id'] , "time": t , "sender" : data["sender"] , "group" : bool(data["group"]) })
                self.db.addRecvMsg( data["id"] , data["sent"] , data["msg"] , t , "text")

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
      
      #groups 
      def create_group(self,gname)  : 
          self.add_send_queue("/create_group",{"gname" : gname})
          time.sleep(0.5) #we will recieve ack in future 
      def add_members(self,gname,members) : 
          members  =  [members] if type(members) != list else members 
          self.add_send_queue("/add_members",{"gname":gname,"members":members})
      def print(self,*args) : 
          logging.info(" ".join(args))       

sock = Client( socket.socket(socket.AF_INET, socket.SOCK_STREAM) , 1)
sock.connect(server_address)
sock.start()
#sock.login_req(input("User : \n"),input("Password : \n"))
sock.login_req(input(""),"123")
count  = 0 
x = []
#x += ["CreateGroup test","AddMember test atishay","AddMember test aadithya"]
#x += ["SendGroup test hi,guys"]
while True : 
     inputs =  { "Send" :  sock.send_msg , "SendGroup" : lambda to,msg : sock.send_msg(to,msg,True) , "CreateGroup" : sock.create_group ,
                  "AddMember" : sock.add_members } #, "PrintRecieved" : sock.print_recv , "PrintSent" : sock.print_sent }     
     
     #i = input("")
     if count >= len(x) : 
        break 
     i = x[count]
     count += 1 
     func = i.split(' ')[0]
     if func  in inputs : 
        inputs[func]( * tuple( i.split(" ")[1: ] ) )
     else : 
      time.sleep(10)
      break 
   


    #  i = input("")
    #  if i == "-1" : 
    #     break 
    #  j = input("")
    #  sock.send_msg(i,j)   
