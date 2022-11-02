from userdb import *

for i in range(0,100):
    signUpUser(f"user{i}",f"pass{i}")

for i in range(0,100,2):
    logInUser(f"user{i}",f"pass{i}",1000+i)

for i in range(0,100,4):
    logOutUser(f"user{i}")

print(checkOnline(f"user{}"))