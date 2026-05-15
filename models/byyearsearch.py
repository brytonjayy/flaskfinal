import mysql.connector
from sshtunnel import SSHTunnelForwarder
with open("stuff.inc") as pwfile:
    mydata = pwfile.readline()
    mydata = mydata.rstrip('\n')
    dblist = mydata.split(" ")  
    dbtuple = tuple(dblist)
    dbuser = dbtuple[1]
    dbpasswd, dbuser, dbname = dbtuple
#print dblist

def getbooksbyyear(searchby, dbuser, dbpasswd, dbname):
    with (SSHTunnelForwarder(("nbtl.mesacc.edu", 787), ssh_pkey="../bry121518.pem", ssh_username=dbuser,
                            remote_bind_address=("localhost", 3306)) as server):

        with mysql.connector.connect(user=dbuser, database=dbname, password=dbpasswd,
                                      host="localhost", port=server.local_bind_port) as db1:

            cursor1 = db1.cursor(buffered=True)
            cursor1.callproc('getbooksbytitle', (searchby,))
            for result in cursor1.stored_results():
                # print(result2.fetchall())
                booklist = []
                for book_id,title,isbn,isbn13,pubyear,pubname in result.fetchall():
                    next_book = {'book_id': book_id, 'title': title, 'isbn': isbn,
                                 'pubyear': pubyear, 'pubname': pubname}
                    booklist.append(next_book)
                    
            return booklist