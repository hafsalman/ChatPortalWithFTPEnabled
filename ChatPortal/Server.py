# from fastapi import FastAPI, HTTPException
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from pydantic import BaseModel
# from DB_Connection.Connection import createConnection

# app = FastAPI()

# class Message(BaseModel):
#     sender: str
#     receiver: str
#     message: str

# def save_message(sender: str, receiver: str, message: str):
#     conn = createConnection()

#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO MESSAGES (sender, receiver, message) VALUES (%s, %s, %s)",
#             (sender, receiver, message)
#         )
#         conn.commit()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to save message to DB")
#     finally:
#         cursor.close()
#         conn.close()

# @app.get("/")
# def read_root():
#     return {"message": "Chat Server is running."}

# @app.post("/send")
# def send_message(msg: Message):
#     save_message(msg.sender, msg.receiver, msg.message)
#     return {"status": "Message stored successfully"}

# @app.get("/messages")
# def get_messages(user: str, since: float):
#     """Get messages sent to this user since a timestamp"""
#     conn = createConnection()
#     if not conn:
#         raise HTTPException(500, "Database connection failed")
    
#     try:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT sender, message FROM MESSAGES "
#             "WHERE receiver = %s AND timestamp > FROM_UNIXTIME(%s) "
#             "ORDER BY timestamp",
#             (user, since)
#         )
#         return cursor.fetchall()
#     finally:
#         cursor.close()
#         conn.close()

# from fastapi import FastAPI, HTTPException, UploadFile, File
# from pydantic import BaseModel
# from DB_Connection.Connection import createConnection
# from ftplib import FTP
# import os

# app = FastAPI()

# class Message(BaseModel):
#     sender: str
#     receiver: str
#     message: str

# def save_message(sender: str, receiver: str, message: str):
#     conn = createConnection()

#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO MESSAGES (sender, receiver, message) VALUES (%s, %s, %s)",
#             (sender, receiver, message)
#         )
#         conn.commit()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to save message to DB")
#     finally:
#         cursor.close()
#         conn.close()

# @app.get("/")
# def read_root():
#     return {"message": "Chat Server is running."}

# @app.post("/send")
# def send_message(msg: Message):
#     save_message(msg.sender, msg.receiver, msg.message)
#     return {"status": "Message stored successfully"}

# @app.get("/messages")
# def get_messages(user: str, since: float):
#     """Get messages sent to this user since a timestamp"""
#     conn = createConnection()
#     if not conn:
#         raise HTTPException(500, "Database connection failed")
    
#     try:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT sender, message FROM MESSAGES "
#             "WHERE receiver = %s AND timestamp > FROM_UNIXTIME(%s) "
#             "ORDER BY timestamp",
#             (user, since)
#         )
#         return cursor.fetchall()
#     finally:
#         cursor.close()
#         conn.close()

# # FTP functions

# def start_ftp_connection():
#     """Returns an FTP connection object"""
#     ftp = FTP()
#     try:
#         ftp.connect("127.0.0.1", 2121)  # Change IP/port if necessary
#         ftp.login("user", "12345")  # Use FTP credentials
#         return ftp
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"FTP connection failed: {str(e)}")

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     ftp = start_ftp_connection()

#     try:
#         # Ensure a directory exists for storing files on FTP
#         ftp.cwd('/')  # Change directory on FTP server
#         ftp.storbinary(f"STOR {file.filename}", file.file)
#         return {"status": "File uploaded successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
#     finally:
#         ftp.quit()

# @app.get("/downloadfile/{filename}")
# async def download_file(filename: str):
#     ftp = start_ftp_connection()

#     try:
#         # Ensure the file exists on the FTP server
#         local_file_path = f"./downloads/{filename}"
#         with open(local_file_path, 'wb') as local_file:
#             ftp.retrbinary(f"RETR {filename}", local_file.write)
#         return {"status": f"File downloaded successfully to {local_file_path}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File download failed: {str(e)}")
#     finally:
#         ftp.quit()

# from fastapi import WebSocket, WebSocketDisconnect
# from typing import List

# active_connections: List[WebSocket] = []

# @app.websocket("/ws/{username}")
# async def websocket_endpoint(websocket: WebSocket, username: str):
#     await websocket.accept()
#     active_connections.append(websocket)
#     await broadcast(f"{username} joined the chat.")

#     try:
#         while True:
#             data = await websocket.receive_text()
#             await broadcast(f"{username}: {data}")
#             save_message(username, "server", data)
#     except WebSocketDisconnect:
#         active_connections.remove(websocket)
#         await broadcast(f"{username} left the chat.")

# async def broadcast(message: str):
#     for connection in active_connections:
#         await connection.send_text(message)

from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from ftplib import FTP
import os

from DB_Connection.Connection import createConnection

app = FastAPI()

# Mount static folder for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve chat page
@app.get("/chat", response_class=HTMLResponse)
def serve_chat():
    with open("static/chat.html", "r") as f:
        return f.read()

# === Models ===
class Message(BaseModel):
    sender: str
    receiver: str
    message: str

# === Active WebSocket Connections ===
active_connections: List[WebSocket] = []

# === WebSocket Chat ===
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections.append(websocket)
    await broadcast(f"{username} joined the chat.")

    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(f"{username}: {data}")
            save_message(username, "server", data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        await broadcast(f"{username} left the chat.")

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)

# === Database Functions ===
def save_message(sender: str, receiver: str, message: str):
    conn = createConnection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO MESSAGES (sender, receiver, message) VALUES (%s, %s, %s)",
            (sender, receiver, message)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save message to DB")
    finally:
        cursor.close()
        conn.close()

# === REST Endpoints ===
@app.get("/")
def read_root():
    return {"message": "Chat Server is running."}

@app.post("/send")
def send_message(msg: Message):
    save_message(msg.sender, msg.receiver, msg.message)
    return {"status": "Message stored successfully"}

@app.get("/messages")
def get_messages(user: str, since: float):
    conn = createConnection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sender, message FROM MESSAGES "
            "WHERE receiver = %s AND m_time > FROM_UNIXTIME(%s) "
            "ORDER BY m_time",
            (user, since)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# === FTP Functions ===
def start_ftp_connection():
    ftp = FTP()
    try:
        ftp.connect("127.0.0.1", 2121)
        ftp.login("user", "12345")
        return ftp
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FTP connection failed: {str(e)}")

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    ftp = start_ftp_connection()
    try:
        ftp.cwd('/')
        ftp.storbinary(f"STOR {file.filename}", file.file)
        return {"status": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    finally:
        ftp.quit()

@app.get("/downloadfile/{filename}")
async def download_file(filename: str):
    ftp = start_ftp_connection()
    try:
        local_file_path = f"./downloads/{filename}"
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        return {"status": f"File downloaded successfully to {local_file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File download failed: {str(e)}")
    finally:
        ftp.quit()