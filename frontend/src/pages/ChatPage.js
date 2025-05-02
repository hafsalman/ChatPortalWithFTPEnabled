import { useState, useEffect } from 'react';
import { sendMessage, getMessages, uploadFile, downloadFile } from '../utils/api';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const username = localStorage.getItem('username');
  const since = 0; // Fetch all messages since epoch (adjust as needed)

  // Fetch messages periodically
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await getMessages(username, since);
        setMessages(response.data);
      } catch (err) {
        setError('Failed to load messages.');
      }
    };

    fetchMessages();
    const interval = setInterval(fetchMessages, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, [username, since]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message) return;

    try {
      await sendMessage(username, 'server', message); // Sending to 'server' as per your DB schema
      setMessage('');
      const response = await getMessages(username, since);
      setMessages(response.data);
    } catch (err) {
      setError('Failed to send message.');
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    try {
      await uploadFile(file);
      alert('File uploaded successfully!');
      setFile(null);
    } catch (err) {
      setError('Failed to upload file.');
    }
  };

  const handleFileDownload = async (filename) => {
    try {
      await downloadFile(filename);
      alert(`File ${filename} downloaded successfully!`);
    } catch (err) {
      setError('Failed to download file.');
    }
  };

  return (
    <div>
      <h2>Chat</h2>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'scroll' }}>
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.sender}:</strong> {msg.message}
          </div>
        ))}
      </div>
      <form onSubmit={handleSendMessage}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
      <h3>File Upload</h3>
      <form onSubmit={handleFileUpload}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>
      <h3>File Download</h3>
      <button onClick={() => handleFileDownload('example.txt')}>
        Download example.txt
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default ChatPage;