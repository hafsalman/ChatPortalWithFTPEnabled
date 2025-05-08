import React from 'react';
import Message from './Message';

function Chat({ messages, onSendMessage, username }) {
  const [message, setMessage] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div style={styles.chatContainer}>
      <h3>Chat</h3>
      <div style={styles.messageArea}>
        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} content={msg.message} isCurrentUser={msg.sender === username} />
        ))}
      </div>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Send</button>
      </form>
    </div>
  );
}

const styles = {
  chatContainer: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '10px',
  },
  messageArea: {
    border: '1px solid #ccc',
    padding: '10px',
    height: '300px',
    overflowY: 'scroll',
    marginBottom: '10px',
  },
  form: {
    display: 'flex',
    gap: '10px',
  },
  input: {
    flex: 1,
    padding: '8px',
    fontSize: '16px',
  },
  button: {
    padding: '8px 16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
};

export default Chat;