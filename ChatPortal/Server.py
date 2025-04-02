import asyncio
import websocket
import mysql.connector
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.Connection import createConnection

session = {}

def MessageHistory():
    conn = createConnection()

    if conn is None:
        return[]
    
    cursor = conn.cursor()