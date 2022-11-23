from connectdb import connectToDB 
conn = connectToDB()

def createGroup(admin,name):
        cur = conn.cursor()  
        cur.execute("SELECT * FROM Groups")
        id = len(cur.fettchall())+1
        cur.execute(f"""INSERT INTO Gropus(ID,NAME,ADMIN,MEMBERS) VALUES ({id},'{name}','{admin}','{admin}')""")
        return id

def addMembers(admin, id, members):
    cur = conn.cursor()
    if (type(members) != list ):
        members = [members]
    cur.execute(f"SELECT MEMBERS FROM Groups WHERE ID = {id} AND ADMIN = {admin}")
    m = cur.fetchone()[0]
    for i in members:
        if (i not in m):
            m = m+","+i
    cur.execute(f"UPDATE Groups SET MEMBERS = '{m}' WHERE ID = {id} AND ADMIN = {admin}")

def getMembers(gname):
    cur = conn.cursor()
    cur.execute(f"SELECT MEMBERS FROM Groups WHERE NAME = '{gname}' ")
    return cur.fetchone()[0]
