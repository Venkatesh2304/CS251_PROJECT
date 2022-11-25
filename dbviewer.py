from connectdb import * 
import pandas as pd 
conn = connectToDB()
cur = conn.cursor()
table = "Users"
cur.execute(f"""SELECT * FROM {table}""")
print( pd.DataFrame(cur.fetchall()) )
# cur.execute("""select column_name
# from information_schema.columns
# where table_name = 'msg_grp_server';
# """)
# print( cur.fetchall() )
