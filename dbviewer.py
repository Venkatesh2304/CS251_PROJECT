from connectdb import * 
import pandas as pd 
conn = connectToDB()
cur = conn.cursor()
x = cur.execute("""SELECT * FROM msg_server""")
print( pd.DataFrame(x) )