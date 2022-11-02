from connectdb import connectToDB
from userdb import *
from createdb import *

conn = connectToDB()

for i in range(1000,1100):
    signUpUser(f"user{i}",f"pass{i}", conn)

for i in range(0,100,2):
    logInUser(f"user{i}",f"pass{i}",1000+i, conn)

for i in range(0,100,4):
    logOutUser(f"user{i}", conn)

print(checkOnline(f"user{2}",conn))