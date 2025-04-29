from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from DB_Connection.Connection import createConnection

app = FastAPI()

class Message(BaseModel):
    sender: str
    receiver: str
    message: str

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