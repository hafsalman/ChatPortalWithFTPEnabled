import mysql.connector
import bcrypt
import sys
import os
from DB_Connection.Connection import createConnection

def LoginUser():
    conn = createConnection()

    if conn is None:
        print