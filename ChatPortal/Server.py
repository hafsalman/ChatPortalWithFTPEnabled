from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from ftplib import FTP
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

app = FastAPI()

# Mount static folder for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve chat page
@app.get("/chat", response_class=HTMLResponse)
def serve_chat():
    try:
        with open("static/chat.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(f"<h3>Error loading chat.html: {str(e)}</h3>", status_code=500)

@app.get("/login", response_class=HTMLResponse)
def serve_login():
    return HTMLResponse("""
    <html><body><h2>Login</h2>
    <form action="/login" method="post">
        Username: <input name="username"><br>
        Password: <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form></body></html>
    """)

@app.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    conn = createConnection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE username = %s AND password_hash = %s", (username, password))
        user = cursor.fetchone()
        if user:
            return {"message": "Login successful"}
        else:
            raise HTTPException(401, "Invalid credentials")
    finally:
        cursor.close()
        conn.close()

@app.get("/register", response_class=HTMLResponse)
def serve_register():
    return HTMLResponse("""
    <html><body><h2>Register</h2>
    <form action="/register" method="post">
        Username: <input name="username"><br>
        Full Name: <input name="full_name"><br>
        Email: <input name="email"><br>
        Password: <input type="password" name="password"><br>
        <button type="submit">Register</button>
    </form></body></html>
    """)

@app.post("/register")
def register_user(username: str = Form(...), full_name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    conn = createConnection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USERS (username, full_name, email, password_hash, registration_date, account_verified)
        VALUES (%s, %s, %s, %s, NOW(), FALSE)
        """, (username, full_name, email, password))
        conn.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(500, f"Registration failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()

class Message(BaseModel):
    sender: str
    receiver: str
    message: str

active_connections: List[WebSocket] = []

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
        try:
            await connection.send_text(message)
        except:
            continue

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
        file_msg = f"<span style='color:#f39c12'>📁 Uploaded: <a href='/downloadfile/{file.filename}' target='_blank'><b>{file.filename}</b></a></span>"
        await broadcast(file_msg)
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
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        return {"status": f"File downloaded successfully to {local_file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File download failed: {str(e)}")
    finally:
        ftp.quit()