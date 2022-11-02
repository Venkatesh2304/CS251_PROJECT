import psycopg2

#signs up a user
def signUpUser(username, password):
    conn = psycopg2.connect(database="test",host="localhost",user="postgres",password="fastchat",port="5432")
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Users WHERE USERNAME='{username}'""")
    if (len(cur.fetchall()) == 0):
        cur.execute(f"""INSERT INTO Users(USERNAME,PASSWORD) VALUES ('{username}','{password}')""")
        conn.commit()
        return True
    return False

#logs in a user
def logInUser(username,password,port):
    conn = psycopg2.connect(database="test",host="localhost",user="postgres",password="fastchat",port="5432")
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM Users WHERE USERNAME='{username}' AND PASSWORD='{password}' """)
    if (len(cur.fetchall()) == 0):
        return False
    else:
        cur.execute(f"""UPDATE Users SET STATUS = 'online', PORT={port} WHERE USERNAME = '{username}' """)
        conn.commit()
        return True

#logs out a user
def logOutUser(username):
    conn = psycopg2.connect(database="test",host="localhost",user="postgres",password="fastchat",port="5432")
    cur = conn.cursor() 
    cur.execute(f"""UPDATE Users SET STATUS = 'offline' WHERE USERNAME = '{username}' """)
    conn.commit()

#checks if a user is online
def checkOnline(username):
    conn = psycopg2.connect(database="test",host="localhost",user="postgres",password="fastchat",port="5432")
    cur = conn.cursor() 
    cur.execute(f"""SELECT * FROM Users WHERE STATUS = 'online' AND USERNAME = '{username}' """)
    if(len(cur.fetchall()) == 0):
        return False
    else:
        return True

