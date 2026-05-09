import mysql.connector
from sshtunnel import SSHTunnelForwarder

def retrieve_user(email, dbuser, dbpasswd, dbname):
    # searchterm should be a dictionary with the keys
    # fname, lname, email, hashpw, status, vcode, vstatus, q1, a1, q2, a2
    with (SSHTunnelForwarder(("nbtl.mesacc.edu", 787), ssh_pkey="E:\\MCC_FILES\\MCC_Classes\\mcccoperni_irsa.pem", ssh_username=dbuser,
                            remote_bind_address=("localhost", 3306)) as server):

        with mysql.connector.connect(user=dbuser, database=dbname, password=dbpasswd,
                                      host="localhost", port=server.local_bind_port) as db1:

            cursor1 = db1.cursor(buffered=True)
            cursor1.callproc('get_customer', (email,))

            for result in cursor1.stored_results():
                for customer_id, fname, lname, email , dateadded, hashpw, status, verifycode, verifystatus in result.fetchall():
                    customer = {'customer_id': customer_id, 'fname': fname, 'lname': lname,
                                'email': email, 'dateadded': dateadded, 'hashpw': hashpw, 'status': status,
                                'verifycode': verifycode, 'verifystatus': verifystatus}

            return customer
