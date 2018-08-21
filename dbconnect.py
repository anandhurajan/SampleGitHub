import  MySQLdb
def connection():
    conn=MySQLdb.connect(host="localhost",user="root",passwd="hdrn59!", db="anandhu_db")
    c=conn.cursor()
    return c,conn

