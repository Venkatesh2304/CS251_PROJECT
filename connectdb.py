import psycopg2

#connects to the database and returns the connection object

def connectToDB():
    conn = psycopg2.connect(database="test",
                        host="localhost",
                        user="postgres",
                        password="fastchat",
                        port="5432")
    return conn