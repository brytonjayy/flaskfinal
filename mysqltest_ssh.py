import mysql.connector
from sshtunnel import SSHTunnelForwarder
# Example based on https://dev.mysql.com/doc/connector-python/en/connector-python-tutorial-cursorbuffered.html
# http://www.mysqltutorial.org/getting-started-mysql-python-connector/
# https://medium.com/@amirziai/query-your-database-over-an-ssh-tunnel-with-pandas-603ce49b35a1

# stuff.inc should have a single line, with three items, with a  single space between them
# mysqlpassword username databasename
# obviously put the ACTUAL password, username and dbname in stuff.inc
with open("stuff.inc") as pwfile:
    mydata = pwfile.readline()
    mydata = mydata.rstrip('\n')
    dblist = mydata.split(" ")
#print dblist

with SSHTunnelForwarder(("nbtl.mesacc.edu", 787), ssh_pkey="bry121518.pem", ssh_username=dblist[1],
                        remote_bind_address=("localhost", 3306)) as server:

    db1 = mysql.connector.connect(user=dblist[1], database=dblist[2], password=dblist[0],
                                  host="localhost", port=server.local_bind_port)

    cursor1 = db1.cursor(buffered=True)
    # prepared=True  will return a byte string  but buffered=True does not
    query = ("Select pubname, publisher_id from grpublishers")
    cursor1.execute(query)

    for (pubname,publisher_id) in cursor1:
        print(f"pub_id: {publisher_id} Publisher: {pubname}")
    db1.close()

    # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
    # note possible need for db1.commit() if doing insert/update etc
    # https://security.openstack.org/guidelines/dg_parameterize-database-queries.html

    db2 = mysql.connector.connect(user=dblist[1], database=dblist[2], password=dblist[0],
                                  host="localhost", port=server.local_bind_port)

    cursor2 = db2.cursor(prepared=True)

    searchterm = input("What is the authors lastname?: ")

    searchterm = searchterm + '%'

    getauthor_stmt = """
    SELECT gb.title,gb.isbn,gb.pubyear,gp.pubname,ga.lastname, ga.firstname,gba.authorder
    FROM grbooks gb JOIN grbooks_authors gba ON (gb.book_id=gba.book_id)
    JOIN grauthors ga ON (ga.author_id=gba.author_id) 
    JOIN grpublishers gp ON (gp.publisher_id=gb.publisher_id)
    Where ga.lastname like %s"""

    cursor2.execute(getauthor_stmt, (searchterm,))

    for (title, isbn, pubyear, pubname, lastname, firstname, authorder) in cursor2:
        print("""
        Title: {0}
        Year: {1}
        Author: {2} {3}
        Isbn: {4}
        ***************************************************
        """.format(title.decode(), pubyear, firstname.decode(), lastname.decode(), isbn.decode()))

    db2.close()
