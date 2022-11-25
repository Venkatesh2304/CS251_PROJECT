from userdb import signUpUser
import msg_serverdb as msg_db
import sys 
import rsa 
import threading
def x(i) : 
        print(i,"started")
        signUpUser(str(i+1),"123")
        # (public_key , private_key) = rsa.newkeys(2048)
        # with open(f"{i+1}.pem","wb+") as f : 
        #     f.write(private_key.save_pkcs1() )
        # msg_db.addPublicKey(str(i+1),public_key.n)

if len(sys.argv) == 2 :
    for i in range(int(sys.argv[1])) : 
        y = threading.Thread(target=x,args=(i,))
        y.start()

      
        
        
          
