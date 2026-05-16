import mysql.connector
from sshtunnel import SSHTunnelForwarder

def getbooksbyauthid(searchterm, dbuser, dbpasswd, dbname):
    with (SSHTunnelForwarder(("nbtl.mesacc.edu", 787), ssh_pkey="bry121518.pem", ssh_username=dbuser,
                            remote_bind_address=("localhost", 3306)) as server):

        with mysql.connector.connect(user=dbuser, database=dbname, password=dbpasswd,
                                      host="localhost", port=server.local_bind_port) as db1:

            cursor1 = db1.cursor(buffered=True)
            cursor1.callproc('getbooksbyauthid', (searchterm,))
            for result in cursor1.stored_results():
                
                booklist = []
                for book_id,title,isbn,isbn13,pubyear,pubname in result.fetchall():
                    next_book = {'book_id': book_id, 'title': title, 'isbn': isbn,
                                 'pubyear': pubyear, 'pubname': pubname}
                    booklist.append(next_book)
                    
            cursor2 = db1.cursor(buffered=True)
            cursor2.callproc('getauthorsbybookid', (searchterm,))
          
            authorlist = []
            for result in cursor2.stored_results():
                for author_id, lastname, firstname, authorder in result.fetchall():
                    next_author = {'author_id': author_id, 'lastname': lastname, 'firstname':firstname,
                                   'authorder': authorder}
                    authorlist.append(next_author)
                    
            booklist.append(authorlist)

            return booklist