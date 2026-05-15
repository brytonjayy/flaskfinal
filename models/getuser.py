import mysql.connector
from sshtunnel import SSHTunnelForwarder

def retrieveuser(email, dbuser, dbpasswd, dbname):
    
    with (SSHTunnelForwarder(("nbtl.mesacc.edu", 787), ssh_pkey="../bry121518.pem", ssh_username=dbuser,
                            remote_bind_address=("localhost", 3306)) as server):

        with mysql.connector.connect(user=dbuser, database=dbname, password=dbpasswd,
                                      host="localhost", port=server.local_bind_port) as db1:

            cursor1 = db1.cursor(buffered=True)
            cursor1.callproc('get_customer', (email,))
            
            for result in cursor1.stored_results():
                for customer_id, fname, lname, email , dateadded, haspw, status, verifycode, verifystatus in result.fetchall():
                    customer = { 'customer_id': customer_id, 'fname': fname, 'lname': lname, 
                                'email': email, 'dateadded': dateadded, 'haspw': haspw, 'status': status, 
                                'verifycode': verifycode, 'verifystatus': verifystatus }
                    
            return customer