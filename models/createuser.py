import mysql.connector
from sshtunnel import SSHTunnelForwarder

def newuser(searchterm, dbuser, dbpasswd, dbname):
    with (SSHTunnelForwarder(("nbtl.mesacc.edu", 787), ssh_pkey="../bry121518.pem", ssh_username=dbuser,
                            remote_bind_address=("localhost", 3306)) as server):

        with mysql.connector.connect(user=dbuser, database=dbname, password=dbpasswd,
                                      host="localhost", port=server.local_bind_port) as db1:
